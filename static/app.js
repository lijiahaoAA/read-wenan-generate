// DOM 元素
const topicInput = document.getElementById('topic');
const customPromptInput = document.getElementById('customPrompt');
const generateBtn = document.getElementById('generateBtn');
const pasteArea = document.getElementById('pasteArea');
const parseBtn = document.getElementById('parseBtn');
const retryBtn = document.getElementById('retryBtn');
const statusSection = document.getElementById('statusSection');
const statusText = document.getElementById('statusText');
const errorSection = document.getElementById('errorSection');
const errorText = document.getElementById('errorText');
const resultSection = document.getElementById('resultSection');
const quotesList = document.getElementById('quotesList');
const saveStatus = document.getElementById('saveStatus');

let isGenerating = false;

// 事件绑定
generateBtn.addEventListener('click', handleGenerate);
parseBtn.addEventListener('click', handleParse);
retryBtn.addEventListener('click', handleRetry);
topicInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !isGenerating) {
        handleGenerate();
    }
});

async function handleGenerate() {
    const topic = topicInput.value.trim();
    const customPrompt = customPromptInput.value.trim();
    
    if (!topic) {
        showError('请输入主题');
        topicInput.focus();
        return;
    }
    
    await generateQuotes(topic, customPrompt);
}

function handleParse() {
    const pastedText = pasteArea.value.trim();
    
    if (!pastedText) {
        showError('请粘贴内容');
        pasteArea.focus();
        return;
    }
    
    try {
        const quotes = parseQuotesFromText(pastedText);
        
        if (quotes.length === 0) {
            showError('未能解析出语录，请检查粘贴的内容格式');
            return;
        }
        
        hideError();
        saveStatus.textContent = `解析成功，共 ${quotes.length} 条语录`;
        saveStatus.className = 'save-indicator';
        displayResults(quotes, false, null);
        
    } catch (error) {
        showError('解析失败: ' + error.message);
    }
}

function parseQuotesFromText(text) {
    const quotes = [];
    const lines = text.split('\n');
    
    for (let line of lines) {
        line = line.trim();
        
        // 匹配格式：1. 语录内容 或 1、语录内容
        const match = line.match(/^\d+[.、]\s*(.+)$/);
        if (match && match[1]) {
            quotes.push(match[1].trim());
        }
    }
    
    return quotes;
}

function handleRetry() {
    hideError();
    topicInput.focus();
}

async function generateQuotes(topic, customPrompt) {
    try {
        const hasCustomPrompt = customPrompt.length > 0;
        
        if (hasCustomPrompt) {
            showLoading('正在生成语录...');
        } else {
            showLoading('正在生成提示词...');
        }
        
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                topic: topic,
                custom_prompt: customPrompt || null
            })
        });
        
        if (!hasCustomPrompt) {
            updateStatus('正在生成语录...');
        }
        
        const data = await response.json();
        
        if (!response.ok || !data.success) {
            throw new Error(data.error || '生成失败');
        }
        
        updateStatus('正在保存到文件...');
        await new Promise(resolve => setTimeout(resolve, 500));
        
        hideLoading();
        displayResults(data.quotes, data.saved, data.save_error);
        
    } catch (error) {
        hideLoading();
        showError(error.message || '生成失败，请重试');
    }
}

function showLoading(message) {
    isGenerating = true;
    generateBtn.disabled = true;
    
    statusText.textContent = message;
    statusSection.style.display = 'block';
    errorSection.style.display = 'none';
    resultSection.style.display = 'none';
}

function updateStatus(message) {
    statusText.textContent = message;
}

function hideLoading() {
    isGenerating = false;
    generateBtn.disabled = false;
    statusSection.style.display = 'none';
}

function showError(message) {
    errorText.textContent = message;
    errorSection.style.display = 'block';
    resultSection.style.display = 'none';
}

function hideError() {
    errorSection.style.display = 'none';
}

function displayResults(quotes, saved, saveError) {
    quotesList.innerHTML = '';
    
    // 显示保存状态
    if (saved) {
        saveStatus.textContent = '✓ 已保存到"文案.md"';
        saveStatus.className = 'save-indicator';
    } else if (saveError) {
        saveStatus.textContent = `⚠ 保存失败: ${saveError}`;
        saveStatus.className = 'save-indicator error';
    }
    
    // 显示语录卡片
    quotes.forEach((quote, index) => {
        const card = document.createElement('div');
        card.className = 'quote-card';
        
        const formattedText = formatQuoteText(quote);
        
        card.innerHTML = `
            <div class="quote-number">NO.${String(index + 1).padStart(2, '0')}</div>
            <div class="quote-text">${formattedText}</div>
            <div class="copy-indicator">点击复制</div>
        `;
        
        card.addEventListener('click', () => {
            copyToClipboard(quote);
        });
        
        quotesList.appendChild(card);
    });
    
    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * 格式化语录文本，在标点符号后智能换行
 */
function formatQuoteText(text) {
    // 在中文标点符号后添加换行
    // 匹配：句号、问号、感叹号、逗号、分号、冒号等
    const formatted = text
        .replace(/([。！？；：，、])/g, '$1<br>')
        .replace(/(<br>)+/g, '<br>') // 移除连续的换行
        .replace(/<br>$/g, ''); // 移除末尾的换行
    
    return formatted;
}

function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            showCopyToast();
        }).catch(() => {
            fallbackCopy(text);
        });
    } else {
        fallbackCopy(text);
    }
}

function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
        document.execCommand('copy');
        showCopyToast();
    } catch (err) {
        console.error('复制失败:', err);
    }
    
    document.body.removeChild(textarea);
}

function showCopyToast() {
    const toast = document.createElement('div');
    toast.className = 'copy-toast';
    toast.textContent = '已复制';
    document.body.appendChild(toast);
    
    setTimeout(() => {
        document.body.removeChild(toast);
    }, 3000);
}

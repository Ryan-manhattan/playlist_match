const PRETEXT_SRC = 'https://esm.sh/@chenglou/pretext@1.2.1';
let pretextModulePromise;

async function loadPretextModule() {
  if (!pretextModulePromise) {
    pretextModulePromise = import(PRETEXT_SRC);
  }
  return pretextModulePromise;
}

function parseFont(element) {
  return element.dataset.pretextFont || window.getComputedStyle(element).font || '16px sans-serif';
}

function parseLineHeight(element, fontSize) {
  const custom = parseFloat(element.dataset.pretextLineHeight);
  if (!isNaN(custom) && custom > 0) {
    return custom;
  }
  const computed = window.getComputedStyle(element).lineHeight;
  if (computed && computed !== 'normal') {
    return parseFloat(computed);
  }
  return fontSize * 1.3;
}

function resolveWidth(element) {
  const attr = element.dataset.pretextWidth;
  if (attr) {
    const parsed = parseFloat(attr);
    if (!isNaN(parsed) && parsed > 0) {
      return parsed;
    }
  }
  const width = element.clientWidth;
  if (width > 0) {
    return width;
  }
  const rect = element.getBoundingClientRect();
  return rect.width || 0;
}

async function measureElement(element) {
  const textSelector = element.dataset.pretextText;
  const sourceElement = textSelector ? element.querySelector(textSelector) : element;
  if (!sourceElement) return null;
  const text = (sourceElement.textContent || '').trim();
  if (!text) return null;
  const width = resolveWidth(element);
  if (!width) return null;
  const font = parseFont(element);
  const fontSize = parseFloat(font) || 16;
  const lineHeight = parseLineHeight(element, fontSize);
  const whiteSpace = element.dataset.pretextWhiteSpace || 'pre-wrap';

  const { prepare, layout } = await loadPretextModule();
  const prepared = prepare(text, font, { whiteSpace });
  const measurement = layout(prepared, width, lineHeight);

  const { height, lineCount } = measurement;
  element.dataset.pretextHeight = height.toFixed(2);
  element.dataset.pretextLines = lineCount;
  element.dataset.pretextFont = font;
  element.dataset.pretextLineHeight = lineHeight;

  if (element.dataset.pretextLineLimit) {
    const limit = parseInt(element.dataset.pretextLineLimit, 10);
    element.classList.toggle('pretext-overflow', limit && lineCount > limit);
  }

  element.style.minHeight = `${Math.ceil(height)}px`;
  element.style.setProperty('--pretext-height', `${height}px`);
  return measurement;
}

async function applyPretextLayout(root = document) {
  const elements = root.querySelectorAll('[data-pretext]');
  if (!elements.length) {
    return [];
  }
  const results = [];
  for (const element of elements) {
    const measurement = await measureElement(element);
    if (measurement) {
      results.push({ element, measurement });
    }
  }
  return results;
}

function debounce(fn, wait = 200) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), wait);
  };
}

const debouncedResize = debounce(() => applyPretextLayout(), 250);
window.addEventListener('resize', debouncedResize);
window.applyPretextLayout = applyPretextLayout;
export { applyPretextLayout };

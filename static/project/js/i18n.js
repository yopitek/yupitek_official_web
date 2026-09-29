/* ==========================================================================
   Yupitek Project Showcase — i18n Translation Engine
   Supports: zh-TW, zh-CN, en, ja, ko
   ========================================================================== */

export const SUPPORTED_LANGS = ['zh-TW', 'zh-CN', 'en', 'ja', 'ko'];
export const DEFAULT_LANG = 'zh-TW';

const LANG_PATH_MAP = {
  'zh-tw': 'zh-TW',
  'zh-cn': 'zh-CN',
  'en': 'en',
  'ja': 'ja',
  'ko': 'ko'
};

const LANG_TO_PATH = {
  'zh-TW': 'zh-tw',
  'zh-CN': 'zh-cn',
  'en': 'en',
  'ja': 'ja',
  'ko': 'ko'
};

let currentLang = DEFAULT_LANG;
let translations = {};

export function detectLanguage() {
  // 1. 從 URL 路徑辨識（例如 /en/solution/project/ -> en）
  const pathParts = window.location.pathname.split('/').filter(Boolean);
  if (pathParts.length > 0) {
    const firstPart = pathParts[0].toLowerCase();
    if (LANG_PATH_MAP[firstPart]) {
      return LANG_PATH_MAP[firstPart];
    }
  }

  // 2. 從 Query 參數辨識 (?lang=...)
  const params = new URLSearchParams(window.location.search);
  const queryLang = params.get('lang');
  if (queryLang) {
    const match = SUPPORTED_LANGS.find(l => l.toLowerCase() === queryLang.toLowerCase());
    if (match) return match;
  }

  // 3. 從 localStorage 辨識
  const stored = localStorage.getItem('yupitek_lang');
  if (stored && SUPPORTED_LANGS.includes(stored)) {
    return stored;
  }

  return DEFAULT_LANG;
}

export async function loadTranslations(lang) {
  try {
    const response = await fetch(`/project/i18n/${lang}.json`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    translations[lang] = await response.json();
    return translations[lang];
  } catch (err) {
    console.warn(`[i18n] Failed to load ${lang}.json, falling back to zh-TW:`, err);
    if (lang !== DEFAULT_LANG) {
      return await loadTranslations(DEFAULT_LANG);
    }
    return null;
  }
}

export function applyTranslations(t) {
  if (!t) return;

  // 更新文本 [data-i18n]
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const val = getNestedValue(t, key);
    if (val !== undefined) {
      el.textContent = val;
    }
  });

  // 更新包含 HTML 標記的欄位 [data-i18n-html]
  document.querySelectorAll('[data-i18n-html]').forEach(el => {
    const key = el.getAttribute('data-i18n-html');
    const val = getNestedValue(t, key);
    if (val !== undefined) {
      el.innerHTML = val;
    }
  });

  // 更新頁面 Title
  if (t.meta && t.meta.title) {
    document.title = t.meta.title;
  }
}

function getNestedValue(obj, keyPath) {
  return keyPath.split('.').reduce((acc, part) => acc && acc[part], obj);
}

export async function switchLanguage(newLang) {
  if (!SUPPORTED_LANGS.includes(newLang)) return;
  currentLang = newLang;
  localStorage.setItem('yupitek_lang', newLang);

  const t = translations[newLang] || await loadTranslations(newLang);
  applyTranslations(t);

  // 更新按鈕 active 狀態
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-lang') === newLang);
  });

  // 溫和更新瀏覽器路徑或記錄
  const targetPrefix = LANG_TO_PATH[newLang];
  const currentPath = window.location.pathname;
  const pathParts = currentPath.split('/').filter(Boolean);
  if (pathParts.length > 0 && LANG_PATH_MAP[pathParts[0].toLowerCase()]) {
    pathParts[0] = targetPrefix;
    const newPath = '/' + pathParts.join('/') + '/';
    if (newPath !== currentPath) {
      window.history.pushState({ lang: newLang }, '', newPath);
    }
  }
}

export async function initI18n() {
  currentLang = detectLanguage();
  const t = await loadTranslations(currentLang);
  applyTranslations(t);

  // 綁定語言切換按鈕事件
  document.querySelectorAll('.lang-btn').forEach(btn => {
    const lang = btn.getAttribute('data-lang');
    btn.classList.toggle('active', lang === currentLang);
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      switchLanguage(lang);
    });
  });
}

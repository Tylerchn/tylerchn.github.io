// Keep links to the former language switch working, including section fragments.
const legacyLanguage = new URL(location.href).searchParams.get('lang');
if (document.documentElement.lang === 'zh-CN' && legacyLanguage === 'en') {
  const english = new URL('./en/', location.href);
  english.hash = location.hash;
  location.replace(english.href);
}

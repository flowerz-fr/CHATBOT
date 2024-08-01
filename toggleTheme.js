const toggleThemeInput = document.getElementById('toggleTheme');
const stylesheet = document.getElementById('themeStylesheet');
const currentTheme = document.getElementById('currentTheme');

toggleThemeInput.addEventListener("change", (e) => {
    stylesheet.href = getStylesheet(e);
    currentTheme.innerText = getInnnerText(e);
})

function getStylesheet(e) {
    if (e.target.checked) return "styleDark.css";
    return "styleLight.css";
}

function getInnnerText(e) {
    if (e.target.checked) return "Dark";
    return "Light";
}
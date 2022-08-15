window.onload = function() {
    //Language
    var language = (window.navigator.languages && window.navigator.languages[0]) ||
    window.navigator.language ||
    window.navigator.userLanguage ||
    window.navigator.browserLanguage;

    console.log(language);

    if (language == 'ja')
        window.location.href = "./ja";
    else
        window.location.href = "./en";
}
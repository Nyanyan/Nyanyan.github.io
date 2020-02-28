(function($) {
    //Language
    var language = (window.navigator.languages && window.navigator.languages[0]) ||
    window.navigator.language ||
    window.navigator.userLanguage ||
    window.navigator.browserLanguage;

    if (language == 'ja')
        window.location.href = "https://nyanyan.github.io/ja/";
    else
        window.location.href = "https://nyanyan.github.io/en/";
})(jQuery);

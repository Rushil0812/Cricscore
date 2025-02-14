if (!document.cookie.includes('user_timezone')) {
    var tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
    document.cookie = "user_timezone=" + tz + "; path=/";
}
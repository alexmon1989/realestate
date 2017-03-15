$("a.sidebar-toggle").click(function () {
    if ($( "body" ).hasClass( "sidebar-collapse" )) {
        Cookies.set('sidebar_size', 'full');
    } else {
        Cookies.set('sidebar_size', 'mini');
    }
});

class Renderer {
    constructor() {}
    render(players) {
        const source = $("#players-template").html();
        const template = Handlebars.compile(source);
        let newHTML = template({ players: players });
        $(".players").empty();
        $(".players").append(newHTML);
    }
}

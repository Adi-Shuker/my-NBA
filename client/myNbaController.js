const renderer = new Renderer();
const players = new Players();
$(".btn-get-team").on("click", () => {
    year = $("#year").val();
    teamName = $("#team-name").val();
    hasBirthDate = $(".has-birth-date")[0].checked;
    players.searchPlayers(year, teamName, hasBirthDate).then((players) => {
        renderer.render(players);
    });
});

$(".btn-dream-team").on("click", () => {
    players.getDreamTeam().then((dreamTeam) => {
        renderer.render(dreamTeam);
    });
});

$("body").on("click", ".add-to-dream-team", function () {
    playerId = $(this).closest("div .card").data().id;
    players.addToDreamTeam(playerId).then((dreamTeam) => {
        renderer.render(dreamTeam);
    });
});

$("body").on("click", ".remove-from-dream-team", function () {
    playerId = $(this).closest("div .card").data().id;
    players.removeFromDreamTeam(playerId).then((dreamTeam) => {
        renderer.render(dreamTeam);
    });
});

$("body").on("click", ".stats", function () {
    playerName = $(this).data().name.split(" ");
    firstName = playerName[0].toLowerCase();
    lastName = playerName[1].toLowerCase();
});

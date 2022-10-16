class Players {
    constructor() {}
    searchPlayers(year, teamName, hasBirthDate) {
        return $.get(
            `/myNBA/players?year=${year}&team=${teamName}&has_birth_date=${hasBirthDate}`
        );
    }
    getDreamTeam() {
        return $.get("/myNBA/dream-team");
    }
    addToDreamTeam(player_id) {
        return $.post(`/myNBA/dream-team/${player_id}`);
    }
    removeFromDreamTeam(player_id) {
        return $.ajax({
            url: `/myNBA/dream-team/${player_id}`,
            type: "DELETE",
            success: function (result) {
                return result;
            },
        });
    }
}

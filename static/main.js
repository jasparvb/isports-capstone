$(async function(){

    const sports = await getSports();
    const leagues = await getLeagues();
    const BASE_URL = "http://127.0.0.1:5000";
    

    async function getSports() {
        const res = await axios.get("https://www.thesportsdb.com/api/v1/json/1/all_sports.php");
        return res.data.sports.map(val => {
            return {label: val.strSport,
                    value: val.strSport,
                    category: "sport",
                    dbid: val.idSport,
                    thumb: val.strSportThumb}
        });
    }
    
    async function getLeagues() {
        const res = await axios.get("https://www.thesportsdb.com/api/v1/json/1/all_leagues.php");
        return res.data.leagues.map(val => {
            return {label: `${val.strLeague} (${val.strSport})`,
                    value: val.strLeague,
                    category: "league",
                    dbid: val.idLeague,
                    thumb: ""}
        });
    }

    async function getTeams(term) {
        const res = await axios.get(`https://www.thesportsdb.com/api/v1/json/1/searchteams.php?t=${term}`);
        if(res.data.teams){
            return teams = res.data.teams.map( val => {
                return {label: `${val.strTeam} - ${val.strLeague} (${val.strCountry})`,
                        value: val.strTeam,
                        category: "team",
                        dbid: val.idTeam,
                        thumb: val.strTeamBadge}
            });
        }
        return [];
    }
    
    async function getPlayers(term) {
        const res = await axios.get(`https://www.thesportsdb.com/api/v1/json/1/searchplayers.php?p=${term}`)
        if(res.data.player){
            return players = res.data.player.map( val => {
                return {label: `${val.strPlayer} (${val.strTeam} - ${val.strPosition})`,
                    value: val.strPlayer,
                    category: "player",
                    dbid: val.idPlayer,
                    thumb: val.strThumb}
                });
            }
        return [];
    }

      $( "#follow-form #name" ).autocomplete({
        minLength: 3,
        source: async function (request, response) {
            let teams = await getTeams(request.term);
            let players = await getPlayers(request.term);
            
            let data = players.concat(teams, sports, leagues);
            response($.ui.autocomplete.filter(data, request.term).slice(0,8));
        },
        // Once a value in the drop down list is selected, do the following:
        select: function(event, ui) {
            // place extra attributes into hidden text fields
            $('#follow-form #tb_image').val(ui.item.thumb);
            $('#follow-form #sportsdb_id').val(ui.item.dbid);
            $('#follow-form #category').val(ui.item.category);
            return false;
        }
      });

    $('body').on('click', '.save-btn', toggleFavorite.bind(this));

    async function toggleFavorite(e) {
        let $this = $(e.target)
        console.log($(e.target).text());
        if($this.text() === "Delete" || $this.text() === "Undo saved") {
            let favoriteId = $this.attr('data-id');

            await axios.delete(`${BASE_URL}/favorites/${favoriteId}`);

            if($this.text() === "Delete") {
                $this.closest('.article').remove();
            } else {
                $this.text('Save');
            }
        }

        if($this.text() === "Save") {
            let title = $this.closest('.card-body').find('h3').text();
            let image_url = $this.closest('.card-body').find('img').attr('src');
            let url = $this.closest('.card-body').find('a').attr('href');
            let published_at = $this.closest('.card-body').attr('data-timestamp');

            const response = await axios.post(`${BASE_URL}/favorites`, {title, url, image_url, published_at});

            console.log(response);
        }

        
    }

});
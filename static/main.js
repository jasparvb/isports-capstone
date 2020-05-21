$(async function(){

    const sports = await getSports();
    const leagues = await getLeagues();
    const BASE_URL = "http://127.0.0.1:5000";
    
    $('body').on('click', '.save-btn', toggleFavorite.bind(this));
    $('body').on('click', '.show-more-btn', loadMoreNews.bind(this));
    $('#language-select').on('change', changeLanguage.bind(this));
    
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
            $('#follow-form #name').val(ui.item.value);
            return false;
        }
    });

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
                //Combine unique words from teamName field and alternate team name field into one array
                let teamNameArr = val.strTeam.split(" ");
                let teamAlternateArr = val.strAlternate.split(" ");

                for(let val of teamNameArr) {
                    if(!teamAlternateArr.includes(val)){
                        teamAlternateArr.push(val)
                    }
                }
                let teamName = teamAlternateArr.join(' ');

                return {label: `${teamName} - ${val.strLeague} (${val.strCountry})`,
                        value: teamName,
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

    //Toggles a article as a favorite when user clicks on save btn
    async function toggleFavorite(e) {
        let $this = $(e.target);
        if($this.hasClass('delete') || $this.hasClass('saved')) {
            let favoriteId = $this.attr('data-id');

            await axios.delete(`${BASE_URL}/favorites/${favoriteId}`);

            if($this.hasClass('delete')) {
                $this.closest('.article').remove();
            } else {
                let url = $this.closest('.card-body').find('a').attr('href');
                //update all identical articles on the page to show as unsaved
                for(let val of $('.card-body').find('a')) {
                    if(val.href === url) {
                        let savedBtn = $(val).next();
                        savedBtn.html('<i class="far fa-plus-square"></i>');
                        savedBtn.removeClass('saved');
                    }
                }
            }
        }
        else {
            let title = $this.closest('.card-body').find('h3').text();
            let image_url = $this.closest('.card-body').find('img').attr('src');
            let url = $this.closest('.card-body').find('a').attr('href');
            let published_at = $this.closest('.card-body').attr('data-timestamp');

            const response = await axios.post(`${BASE_URL}/favorites`, {title, url, image_url, published_at});

            //update all identical articles on the page to show as saved
            for(let val of $('.card-body').find('a')) {
                if(val.href === url) {
                    let savedBtn = $(val).next();
                    savedBtn.attr('data-id', response.data.favorite.id);
                    savedBtn.html('<i class="far fa-minus-square"></i>');
                    savedBtn.addClass('saved');
                }
            }
        }
    }

    //Retrieves 7 more news articles when user clicks 'Show More' btn and adds them to the DOM
    async function loadMoreNews(e) {
        let $this = $(e.target);
        let page = $this.attr('data-page');
        let term = $this.attr('data-term');
        page = parseInt(page) + 1;

        const response = await axios.post(`${BASE_URL}/news`, {page, term});
        
        if(response.data.articles[0]){
            for(let article of response.data.articles) {
                let newArticle = generateHTML(article);
                console.log(newArticle.html());
                $this.closest('.row').prev().append(newArticle);
            }
            $this.attr('data-page', page);
        } else {
            $this.remove();
        }
        await updateFavorites();
        //Remove save btn when user is not logged in
        if(!$('unauthorized').length){
            for(let val of $('.save-btn')) {
                val.remove();
            }
        }
    }

    function generateHTML(article) {
        let $item = $(`
        <div class="my-3 col-12 col-md-4 col-news article">
            <div class="card">
                <div class="card-body text-center" data-timestamp="${article.publishedAt}">
                    <a href="${article.url}" target="_blank">
                    <img src="${article.urlToImage}" alt="">
                    <h3>${article.title}</h3></a>
                    <button data-id="" class="btn btn-sm btn-red save-btn"><i class="far fa-plus-square"></i></button>
                </div>
            </div>
        </div>
        `);
        return $item;
    }

    async function updateFavorites() {
        const response = 1
    }

    async function changeLanguage(e) {
        let language = $(e.target).val();
        const response = await axios.post(`${BASE_URL}/language`, {language});
        window.location.href = window.location.pathname + window.location.search + window.location.hash;
        console.log(response);
    }

});
var aktuAlbum='';
var aktuJahr='';
var aktuMonat='';
var aktuTag='';

$("Dokument").ready(function(){
    $.getJSON('q/album', '', function(antwort){
        var s='';
        for (var i in antwort.Alben)
            s+='<option value="'+antwort.Alben[i].Album+'">'+antwort.Alben[i].Name+'</option>';
        $("#album").html(s).click(function(){
            getJahre();
        });
        getJahre();
    })
});

function getJahre(){
    var s=$('#album').val();
    if (s!=aktuAlbum) {
        aktuAlbum=s;
        $.getJSON('q/jahre', {
            Album: aktuAlbum
        }, function(antwort){
            var s='';
            var max=antwort.Jahre.length -1;
            for (var i in antwort.Jahre)
                if (i==max)
                    s+='<option selected value="'+antwort.Jahre[i].Jahr+'">'+antwort.Jahre[i].Jahr+'</option>';
                else
                    s+='<option value="'+antwort.Jahre[i].Jahr+'">'+antwort.Jahre[i].Jahr+'</option>';
            $('#jahr').html(s).click(function(){
                getMonat();
            })
            aktuJahr='';
            getMonat();
        });
    }
}

function getMonat(){
    var s=$('#jahr').val();
    if (s!=aktuJahr) {
        aktuJahr=s;
        $.getJSON('q/monat', {
            Album: aktuAlbum,
            Jahr: aktuJahr
        }, function(antwort){
            var s='';
            var max=antwort.Monate.length -1;
            for (var i in antwort.Monate)
                if (i==max)
                    s+='<option selected value="'+antwort.Monate[i].Monat+'">'+antwort.Monate[i].Name+'</option>';
                else
                    s+='<option value="'+antwort.Monate[i].Monat+'">'+antwort.Monate[i].Name+'</option>';
            $('#monat').html(s).click(function(){
                getTage();
            })
            aktuMonat='';
            getTage();
        })
    }
}

function getTage(){
    var s=$('#monat').val();
    if (s!=aktuMonat) {
        aktuMonat=s;
        $.getJSON('q/tage', {
            Album: aktuAlbum,
            Jahr: aktuJahr,
            Monat: aktuMonat
        }, function(antwort){
            var s='';
            var max=antwort.Tage.length -1;
            for (var i in antwort.Tage)
                if (i==max)
                    s+='<option selected value="'+antwort.Tage[i].Verzeichnis+'">'+antwort.Tage[i].Name+'</option>';
                else
                    s+='<option value="'+antwort.Tage[i].Verzeichnis+'">'+antwort.Tage[i].Name+'</option>';
            $('#tage').html(s).click(function(){
                getBilder();
            })
            aktuTag='';
            getBilder();

        })
    }
}

function getBilder(){
    var s=$('#tage').val();
    if (s!=aktuTag) {
        aktuTag=s;
        $.getJSON('q/bilder', {
            Album: aktuAlbum,
            Jahr: aktuJahr,
            Monat: aktuMonat,
            Tag: aktuTag
        }, function(antwort){

            })
        }
}
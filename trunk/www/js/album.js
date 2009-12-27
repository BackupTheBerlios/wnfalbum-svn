var aktuAlbum='';
var aktuJahr='';
var aktuMonat='';

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
        $.getJSON('q/jahre', {Album: aktuAlbum}, function(antwort){
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
        $.getJSON('q/monat', {Album: aktuAlbum,Jahr: aktuJahr}, function(antwort){

            })
    }
}
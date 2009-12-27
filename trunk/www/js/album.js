var aktuAlbum='';

$("Dokument").ready(function(){
    $.getJSON('q/album', '', function(alben){
        var s='';
        for (var i in alben.Alben)
            s+='<option value="'+alben.Alben[i].Album+'">'+alben.Alben[i].Name+'</option>';
        $("#album").html(s).click(function(){
            getJahre();
        });
        getJahre();
    })
});

function getJahre(){
    var s=$("#album").val();
    if (s!=aktuAlbum) {
     aktuAlbum=s;
     $.getJSON('q/jahre', 'album='+aktuAlbum, function(){
         
     })

    }

}
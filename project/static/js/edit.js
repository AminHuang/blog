
$(document).ready(function(){

    $("#subcontent").click(function(){
        savaBlog();
    });

    $("#cancel").click(function(){
        
    });
});

// 去除收尾双引号
// function fTrim(str) {
//  str=str.replace(/(^\s*")|("\s*$)/g, ""); 
//  return str;
// }

function getContent() {
    var arr = [];
    arr.push("使用editor.getContent()方法可以获得编辑器内容");
    arr.push("内容为：");
    arr.push(UE.getEditor('editor').getContent());
    alert(arr.join("\n"));
}


function savaBlog() {
	var blogcontent = UE.getEditor('editor').getPlainTxt();
    // blogcontent = fTrim(blogcontent);
    var titlecontent = $("#title").val();
    alert(titlecontent);
    $.ajax({
    	type: 'post',
        url : $SCRIPT_ROOT + '/save_blog',
        dataType: 'json',
        data : 'content=' + blogcontent + '&title=' +  titlecontent,
        success : function() {
        	alert('ok');
        },
        error : function(json) {
        	alert("error");
        }
    });

}

function getPlainTxt() {
        var arr = [];
        arr.push("使用editor.getPlainTxt()方法可以获得编辑器的带格式的纯文本内容");
        arr.push("内容为：");
        arr.push(UE.getEditor('editor').getPlainTxt());
        alert(arr.join('\n'))
    }

function getContentTxt() {
        var arr = [];
        arr.push("使用editor.getContentTxt()方法可以获得编辑器的纯文本内容");
        arr.push("编辑器的纯文本内容为：");
        arr.push(UE.getEditor('editor').getContentTxt());
        alert(arr.join("\n"));
    }


function getContent() {
    var arr = [];
    arr.push("使用editor.getContent()方法可以获得编辑器内容");
    arr.push("内容为：");
    arr.push(UE.getEditor('editor').getContent());
    alert(arr.join("\n"));
}

function prettyDate(time){if(time){var date=new Date((time||"").replace(" ", "T")),diff=(((new Date()).getTime()- date.getTime())/1000),day_diff=Math.floor(diff/86400);if(isNaN(day_diff)||day_diff<0)
return"剛剛";return day_diff==0&&(diff<60&&"剛剛"||diff<120&&"1分鐘前"||diff<3600&&Math.floor(diff/60)+"分鐘前"||diff<7200&&"1小時前"||diff<86400&&Math.floor(diff/3600)+"小時前")||day_diff==1&&"昨天"||day_diff<7&&day_diff+"天前"||day_diff<31&&Math.ceil(day_diff/7)+"週前"||day_diff<365&&Math.ceil(day_diff/31)+"個月前"||day_diff>=365&&Math.ceil(day_diff/365)+"年前";}
return"";}
if(typeof jQuery!="undefined")
jQuery.fn.prettyDate=function(){return this.each(function(){var date=prettyDate(this.title);if(date)
jQuery(this).text(date);jQuery(this).attr("title","");});};
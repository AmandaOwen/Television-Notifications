function SelectType(channels) 
{
	$(".normal").each( function() 
	{
		$(this).attr("checked",false);	
	}	
	)
	$(channels).each ( function() 
	{ 
		$(this).attr("checked", "checked");
	}
	)
}

function Unselect() 
{
	$(".normal").each( function() 
	{
		$(this).attr("checked",false);	
	}	
	)
}
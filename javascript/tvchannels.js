function SelectFreeview() 
{
	$(".normal").each( function() 
	{
		$(this).attr("checked",false);	
	}	
	)
	$(".freeview").each ( function() 
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
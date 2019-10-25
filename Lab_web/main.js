function page(id)
{
  document.getElementById("navigator_bar").getElementsByTagName("h1")[id].setAttribute("class","selected_page");

  for(var i=0;i<document.getElementById("navigator_bar").getElementsByTagName("h1").length;i++)
  {
     if(i != id)
     {
       document.getElementById("navigator_bar").getElementsByTagName("h1")[i].setAttribute("class","unselect_page");
     }
  }

  if(id==0)
  {
    document.getElementById("home").setAttribute("style","display:block; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_news").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("professor").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("publication_and_project").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("research_area").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_research").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
  }
  else if(id==1)
  {
    document.getElementById("home").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_news").setAttribute("style","display:block; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("professor").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("publication_and_project").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("research_area").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_research").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
  }
  else if(id==2)
  {
    document.getElementById("home").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_news").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("professor").setAttribute("style","display:block; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("publication_and_project").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("research_area").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_research").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
  }
  else if(id==3)
  {
    document.getElementById("home").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_news").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("professor").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("publication_and_project").setAttribute("style","display:block; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("research_area").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_research").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
  }
  else if(id==4)
  {
    document.getElementById("home").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_news").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("professor").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("publication_and_project").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("research_area").setAttribute("style","display:block; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_research").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
  }
  else if(id==5)
  {
    document.getElementById("home").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_news").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("professor").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("publication_and_project").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("research_area").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_research").setAttribute("style","display:block; padding:0px; margin: 0px; width: 99vw;");
  }
  else
  {
    document.getElementById("home").setAttribute("style","display:block; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_news").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("professor").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("publication_and_project").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("research_area").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
    document.getElementById("latest_research").setAttribute("style","display:none; padding:0px; margin: 0px; width: 99vw;");
  }

}

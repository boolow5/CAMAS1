
    
		function getMarks(){
		  subjects = getElementsByClassName("subject");
		  var total = Array(0);
		  for (var i=0; i<subjects.length;i++){
		   subs = document.getElementsByClassName(subjects[i]+"-marks");
		   //console.log(subs.length);
		   var subject_total = 0;
		   for (var j=0; j<subs.length; j++){
		   //console.log(subs);
		     if(! isNaN(parseFloat(subs[j].innerHTML))){
		       subject_total += parseFloat(subs[j].innerHTML);
		       //console.log(subject_total);
		     }
		   }
		  //console.log(subject_total);
		   total.push(subject_total);
		  }
		  
		  for(var k=0; k<subjects.length;k++){
		    element1 = document.getElementById(subjects[k]+'-marks-total');
		    element1.innerHTML = total[k];
		    console.log(total[k]);
		  }
		  
		  return total;
		}
    
    function showWidth() {
        alert($('#English-marks-total').width());
    }
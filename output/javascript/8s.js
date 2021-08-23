winning_arr = [["1","2","3"],["4","5","6"],["7","8","x"]];
arr = init_arr();
flag = false;
moves = 0;

window.onload = function () {
    display_arr(arr);
}

$(document).keydown(function(e) {
    doMove(e.which);
});

//Should probably enum the moves
function doMove(move){
    process_input(arr, move);
    display_arr(arr);  
    flag = JSON.stringify(arr) == JSON.stringify(winning_arr);
    if(flag){
        document.getElementById("msg").text = "Winner winner in " + moves + " moves (Press 'r' to reset)";
    }else{
        document.getElementById("msg").text = "" + moves + " moves";        
    }
}

//Shamelessly stolen from stack overflow
function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}

//Initialize
function init_arr(){
    //init random array
    options= ["1","2","3","4","5","6","7","8","x"]
    shuffleArray(options)
    //this will get overwritten, initializing to get the shape
    arr = [["1","2","3"],["4","5","6"],["7","8","x"]]
    x = -1
    y = -1
    for(let i = 0; i < 3; i++) {
        for(let j = 0; j < 3; j++){
            val = options[i * 3 + j]
            arr[i][j] = val
            if(val == "x"){
                x = i;
                y = j;
            }
        }
    }
    return arr;
}

//Reset
function reset(){
    moves = 0;
    arr = init_arr();
    flag = false;
    document.getElementById("msg").text = "0 moves";
    display_arr(arr);
}

//Just swap in the direction we push (or reset on "R" and "Enter")
function process_input(arr, key){    
    if(key == 82 | key == 13){ 
        reset();
    }
    if(!flag){
        if(key == 37){ //left
            if(y > 0){ 
                arr[x][y] = arr[x][y-1]
                y = y - 1
                arr[x][y] = 'x'
                moves++;
            }
        }
        else if(key == 39){ //right
            if(y < 2){
                arr[x][y] = arr[x][y+1]
                y = y + 1
                arr[x][y] = 'x'
                moves++;
            }
        }
        else if (key == 38){ //up
            if(x > 0){
                arr[x][y] = arr[x-1][y]
                x = x - 1
                arr[x][y] = 'x'
                moves++;
            }
            
        }
        else if (key == 40){ //down
            if(x < 2){
                arr[x][y] = arr[x+1][y]
                x = x + 1
                arr[x][y] = 'x'
                moves++;
            }
        }
    }
    return arr;   
}

//Update the display
function display_arr(arr){
    for(let i = 0; i < 3; i++) {
        var txt = ""
        for(let j = 0; j < 3; j++){
            txt += arr[i][j];
        }
        document.getElementById("r" + (i+1)).text = txt;
    }
}

//TOUCH STUFF
document.addEventListener('touchstart', handleTouchStart, false);        
document.addEventListener('touchmove', handleTouchMove, false);

var xDown = null;                                                        
var yDown = null;

function getTouches(evt) {
  return evt.touches ||             // browser API
         evt.originalEvent.touches; // jQuery
};                                                     
                                                                         
function handleTouchStart(evt) {
    const firstTouch = getTouches(evt)[0];                                      
    xDown = firstTouch.clientX;                                      
    yDown = firstTouch.clientY;                                      
};                                                
                                                                         
function handleTouchMove(evt) {
    if ( ! xDown || ! yDown ) {
        return;
    }

    var xUp = evt.touches[0].clientX;                                    
    var yUp = evt.touches[0].clientY;

    var xDiff = xDown - xUp;
    var yDiff = yDown - yUp;
                              
    mv = -1;
    if ( Math.abs( xDiff ) > Math.abs( yDiff ) ) {/*most significant*/
        if ( xDiff > 0 ) {
            /* right swipe */ 
            doMove(37); //right
        } else {
            /* left swipe */
            doMove(39);
        }                       
    } else {
        if ( yDiff > 0 ) {
            /* down swipe */
            doMove(38); 
        } else { 
            /* up swipe */
            doMove(40);
        }                                                                 
    }
    /* reset values */
    xDown = null;
    yDown = null;                                             
};

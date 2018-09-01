#include <stdio.h>
//#include <wiringPi.h>

void laserMove(int*,int*,int*,int*,int*,int,int);


int main(){
    
    //wiringPiSetupGpio();
    
    int x[4] = {1,2,3,4};
    int xn[4] = {1,2,3,4};
    int y[4] = {1,2,3,4};
    int laserPin = 1;
    
    int xcoord;
    int ycoord;
    
    int pxcoord = 34;
    int pycoord = 42;
    
    char buffer;
    
    int exit = 0;
    
    /*
     digitalWrite(x[0], LOW);
     digitalWrite(x[1], LOW);
     digitalWrite(x[2], LOW);
     digitalWrite(x[3], LOW);
     
     digitalWrite(xn[0], LOW);
     digitalWrite(xn[1], LOW);
     digitalWrite(xn[2], LOW);
     digitalWrite(xn[3], LOW);
     
     digitalWrite(y[0], LOW);
     digitalWrite(y[1], LOW);
     digitalWrite(y[2], LOW);
     digitalWrite(y[3], LOW);
     */
    
    while(exit==0){
        
    
        printf("Type in x coordinate followed by y coordinate: ");
        scanf("%d,%d",&xcoord,&ycoord);
        scanf("%c",&buffer);
    
        printf("%d and %d\n",xcoord,ycoord);
        
        if(xcoord == -1)
            exit = 1;
        else{
            laserMove(&x[0],&xn[0],&y[0],&pxcoord,&pycoord,xcoord,ycoord);
        }
        
        printf("%d\n",pxcoord);
        
    }

    
    return 0;
}


void laserMove(int *x, int *xn, int *y, int *pxcoord, int *pycoord, int xcoord, int ycoord){
    
    int cx;
    int cy;
    int xdist;
    int ydist;
    int dist;
    int i;
    dist = 0;
    
    
    if(xcoord > *pxcoord){
        cx = 1;
        dist = xcoord - *pxcoord;}
    else if(xcoord < *pxcoord){
        cx = -1;
        dist = *pxcoord - xcoord;}
    else
        cx = 0;
    
    
    if(ycoord > *pycoord){
        cy = 1;
        dist = ycoord - *pycoord;}
    else if(ycoord < *pycoord){
        cy = -1;
        dist = *pycoord - ycoord;}
    else
        cy = 0;
    
    xdist = *pxcoord;
    ydist = *pycoord;
    
    
    for(i=0;i<dist;i++){
        /*
         digitalWrite(x[xdist%4],HIGH);
         digitalWrite(x[(xdist-cx)%4],LOW);
         
         digitalWrite(xn[xdist%4],HIGH);
         digitalWrite(xn[(xdist-cx)%4],LOW);
         
         digitalWrite(y[ydist%4],HIGH);
         digitalWrite(y[(ydist-cy)%4],LOW);
         
         */
        
        xdist = xdist + cx;
        ydist = ydist + cy;
    }
    
    *pxcoord = xdist;
    *pycoord = ydist;
}


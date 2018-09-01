#include <stdio.h>
#include <math.h>
//#include <wiringPi.h>

void laserMove(int*,int*,int*,int*,int*,int,int);


int main(){
    
    //wiringPiSetupGpio();
    
    int x[4] = {17,18,23,24};
    int xn[4] = {2,14,4,3};
    int y[4] = {9,10,11,25};
    int laserPin = 21;
    
    int xcoord;
    int ycoord;
    int pxcoord = 0;
    int pycoord = 0;
    
    char buffer;
    int exit = 0;
    
    int pstate = 2;
    int state = 2;
    
    double xstep[200];
    double ystep[200];
    int ixstep[200];
    int iystep[200];
    int type[200];
    char input[140];
    int i;
    int ii=0;
    
    double key=100.0;
    
    double sum;
    
    FILE *top;
    
    /*
    pinMode(x[0], OUTPUT);
    pinMode(x[1], OUTPUT);
    pinMode(x[2], OUTPUT);
    pinMode(x[3], OUTPUT);
    
    pinMode(xn[0], OUTPUT);
    pinMode(xn[1], OUTPUT);
    pinMode(xn[2], OUTPUT);
    pinMode(xn[3], OUTPUT);
    
    pinMode(y[0], OUTPUT);
    pinMode(y[1], OUTPUT);
    pinMode(y[2], OUTPUT);
    pinMode(y[3], OUTPUT);
    
    pinMode(laserPin, OUTPUT);
    
    
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
    
    
    if((top = fopen("file.txt","r"))==NULL)
        printf("Error opening file.\n");
    else{
        while(!feof(top)){
            fscanf(top,"%s",input);
            if(input[0]=='X'){
                sum = 0.0;
                for(i=0;i<7;i++){
                    sum= sum + ((double) input[i+1] - 48)*pow(10.0,(1-i));
                }
                //printf("%7.5f\t",sum);
                ystep[ii] = sum;
                
                sum = 0.0;
                for(i=0;i<7;i++){
                    sum= sum + ((double) input[i+9] - 48)*pow(10.0,(1-i));
                }
                xstep[ii] = sum;
                
                
                type[ii] = input[18]-48;
                
                ii = ii+1;
            }
        }
        
        for(i=0;i<ii;i++){
            
            ixstep[i] = (int)(xstep[i]*key)*10;
            //printf("%d\n",ixstep[i]);
            
            if(((xstep[i]*key*10.0)-((double) ixstep[i]))>=5.0)
                ixstep[i] = (int) (xstep[i]*key)+1;
            else
                ixstep[i] = (int) (xstep[i]*key);
            
            iystep[i] = (int)(ystep[i]*key)*10;
            //printf("%d\n",ixstep[i]);
            
            if(((ystep[i]*key*10.0)-((double) iystep[i]))>=5.0)
                iystep[i] = (int) (ystep[i]*key)+1;
            else
                iystep[i] = (int) (ystep[i]*key);
            
            state = type[i];
            
            
            
            if(pstate == state){}
            else if(state == 1){
                //digitalWrite(laserPin, HIGH);
            }
            else{
                //digitalWrite(laserPin,LOW);
            }
        
                
            
            //laserMove(&x[0],&xn[0],&y[0],&pxcoord,&pycoord,ixstep[i],iystep[i]);
            printf("%7.5f\t\t%7.5f\t\t%d\t\t%d\t\t%d\n",xstep[i],ystep[i], type[i],ixstep[i],iystep[i]);
        }
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
         
         
        
        xdist = xdist + cx;
        ydist = ydist + cy;
        
        delay(35);
         */
    }
    
    *pxcoord = xdist;
    *pycoord = ydist;
}

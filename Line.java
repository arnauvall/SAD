import java.io.*;
import java.lang.StringBuilder.*;

public class Line{
    int pos = 0;
    StringBuilder text=new StringBuilder("");
    boolean ins=false;
    
    public void addChar(char c){
        StringBuilder strb = new StringBuilder(text);
        if(ins && (pos < text.length())){
            //Introducimos el caracter en la posición en la que nos encontramos
            strb.setCharAt(pos,c);
        }
        else{
            strb.insert(this.pos, c);
        }

    }

    public void delChar(int del){
        if(this.pos >= 0 && !this.text.toString().isEmpty()){
            this.text = this.text.delete(this.pos+del, this.pos+del+1);
            this.pos+=del;
        }
    }

    public void print(){
         System.out.print("\033[H\033[2J"); //clear pantalla
         System.out.print(this.text);
         //System.out.print(); //move cursor a la pos

    }
}

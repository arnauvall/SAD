import java.io.*;
import java.awt.*;

class EditableBufferedReader extends BufferedReader{

	static final int L=37; //<-- in ASCII
	static final int R=39;   //--> in ASCII
	//static final int modo=;
	//static final int ini=;
	//static final int fin=;
	static final int del=8;
//	static final int supr=;
	//static final int ins=;
	static final int EOF=13;
	private Line line = new Line();

	//MIRAR EL CONSTRUCTOOR, NS COMO HACERLO
	public EditableBufferedReader(Reader in){
		super(in);
	}

	private void setRaw() throws IOException{
		//comando de terminal stty -echo raw
		// /dev/tty --> para referirnos al terminal del proceso actual
		try{
		String[] cmd = {"/bin/sh", "-c", "stty -echo raw </dev/tty"};
		Runtime.getRuntime().exec(cmd).waitFor();
		}catch(IOException e){
		}
	}

	private void unsetRaw() throws IOException{
		//comando de terminal reset
		// /dev/tty --> para referirnos al terminal del proceso actual
		try{
		String[] cmd = {"/bin/sh", "-c", "reset </dev/tty"};
		Runtime.getRuntime().exec(cmd).waitFor();
		}catch(IOException e){

		}
	}

	@Override
	public int read(){
		try{
			//Para leer el siguiente caracter, dado que estamos en Raw
			//envia cada tecla que escribimos
			this.setRaw();
			return super.read();
		}
		finally{
			this.unsetRaw();
		}
	}
	@Override
	public String readLine(){
		int c;
		c=this.read();
		while(c!=EOF){
			switch(c){
				case R:
					line.pos += 1;
					break;
				case L: 
					line.pos -= 1;
					break;
		/*		case ini:
					line.pos = 0;
					break;
				case fin:
					line.pos = size(line.text);
					break;
				case ins:
					line.ins != line.ins;
					break;*/
				case del:
					line.delChar(0);
					break;
			/*	case supr:
					if(line.pos!=size(line.text)){
						line.delChar(1);
					}
					break;*/
				default:
					line.addChar((char)c);
					break;
			}
			line.print();
			c = this.read();
		}

		return line.text.toString();

	}
} 

package taallocation;


import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
 
public class readcsv {

 ArrayList<ArrayList> data= new ArrayList<>();
 String filename;
 
  public ArrayList<ArrayList> imp(String name) {
 filename=name;
	readcsv obj = new readcsv();
	obj.run(data,filename);
 return data;
  }
 
  public static void run( ArrayList<ArrayList> data1, String nam) {
 
	String csvFile = nam;
	BufferedReader br = null;
	String line = "";
	String cvsSplitBy = ",";
 
	try {
 
		
 
		br = new BufferedReader(new FileReader(csvFile));
              
		while ((line = br.readLine()) != null) {
  ArrayList<Object> temp =new ArrayList<>();
			// use comma as separator
			String[] d = line.split(cvsSplitBy);
 
			for(int i=0;i<d.length;i++){
                            temp.add(d[i]);
                        }
                        
                        temp.remove(0);
                        data1.add(temp);
                       
                        
                 
		}
 
			
 
		
 
	} catch (FileNotFoundException e) {
		e.printStackTrace();
	} catch (IOException e) {
		e.printStackTrace();
	} finally {
		if (br != null) {
			try {
				br.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
 
	
  }
 
}
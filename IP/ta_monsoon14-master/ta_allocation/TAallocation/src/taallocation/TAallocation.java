/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package taallocation;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;
import taallocation.TAallocation;


/**
 *
 * @author sourabh
 */
public class TAallocation {

    /**
     * @param args the command line arguments
     * 
     */
    
    
    public static void main(String[] args) throws IOException {
       
        
         String s = null;
        ArrayList<int[][]> in=new ArrayList<>();
         int[][] Man;
    int[][] Woman;
     int []rgs;
        
         NewClass n=new NewClass();
        try {
            Scanner input = new Scanner(System.in);

      System.out.println("Enter a string");
      s = input.nextLine();
            //D:\\TAallocation\\
            n.main(s);
        } catch (IOException ex) {
            Logger.getLogger(TAallocation.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        Ta m=new Ta();
       int[] retrn= m.main();
        
        
        
         int men=retrn[0];
   int  women=retrn[1];
   
   
  
   System.out.println(men);
   System.out.println(women);
   read r=new read(men,women);
                try {
                    in=r.main(men, women);
                } catch (IOException ex) {
                   
                }
                
         Man=in.get(0);
         Woman=in.get(1);
         
        gs g=new gs(men,women,Man,Woman);
        rgs=g.imp(men,women,Man,Woman);  
        
        System.out.println(men+"m"+women);
        ArrayList<ArrayList> all= new ArrayList<>();
                                                            //women:students
                                                            //men:courses
       String st[]=new String[women];
       String cs[]=new String[men];
        for(int i=0;i<women;i++)
        { 
              st[i]=n.students.get(i+1).get(0).toString();
               System.out.println(st[i]);    
               }
        System.out.println(n.course_details+"size"+n.course_details.get(0).size()); 
        int x=0;
         for(int i=0;i<(n.course_details.get(0).size());i++)
        { 
           // System.out.println(Integer.parseInt(n.course_details.get(2).get(i).toString())); 
            for(int j=0;j<Integer.parseInt(n.course_details.get(2).get(i).toString());j++)
            { cs[x]=n.course_details.get(0).get(i).toString();
               System.out.println(cs[x]); 
               x++;
            }
               }
         
         
          BufferedWriter br = new BufferedWriter(new FileWriter(s+"final.csv"));

for(int t=0;t<rgs.length;t++){
  
br.write(st[t]+","+cs[rgs[t]]);
br.newLine();
}       
 br.close();
         
    }
       
    }


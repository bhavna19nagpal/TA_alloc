package taallocation;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */


import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

/**
 *
 * @author sourabh
 */
public class NewClass {
           ArrayList<ArrayList> course= new ArrayList<>();
           ArrayList<ArrayList> students= new ArrayList<>();
               ArrayList<ArrayList> skills= new ArrayList<>();
                ArrayList<ArrayList> prereqs  = new ArrayList<>();
                ArrayList<ArrayList> preferences  = new ArrayList<>();
                ArrayList<ArrayList> course_details  = new ArrayList<>();
                   ArrayList<ArrayList> shortlist  = new ArrayList<>();
    public  void main(String path) throws IOException{
        double skillwt=0.2;
       double prefwt=0.3;
       double coursewt=0.3;
       double preqwt=0.2;
            
        double[][] utility = new double[190][190];
        for(int yt1=0; yt1<utility.length;yt1++){
            for(int ty=0;ty<utility[0].length;ty++){
                utility[yt1][ty]=-1;
            }
    
}
         readcsv n=new readcsv();
        
             BufferedReader br1 = null;
        br1 = new BufferedReader(new FileReader(path+"preferences.csv"));
          String line = "";
	String cvsSplitBy = ",";    
		while ((line = br1.readLine()) != null) {
  ArrayList<Object> temp =new ArrayList<>();
			// use comma as separator
			String[] d = line.split(",");
 
			for(int i=0;i<d.length;i++){
                            temp.add(d[i]);
                        }
                        
                        //temp.remove(0);
                        students.add(temp);
                       
                        
                 
		}    
             course=  n.imp(path+"courses.csv");
             readcsv n1=new readcsv();
             prereqs=n1.imp(path+"prereqs.csv");
             readcsv n2=new readcsv();
            
             skills = n2.imp(path+"skills.csv");
             readcsv n3=new readcsv();
             
             preferences= n3.imp(path+"preferences.csv");
             // System.out.println(preferences.size());
             readcsv n4=new readcsv();
             course_details= n4.imp(path+"course_details.csv");
             int totalstudents=course.size();
             readcsv n5=new readcsv();
             
             shortlist= n5.imp(path+"shortlist.csv");
            
             int i1=0;
             for(int i=0;i< course_details.get(0).size();i++){
                String coursename= (String) course_details.get(0).get(i);
                String pre= (String) course_details.get(3).get(i);
                String skil= (String) course_details.get(4).get(i);
                String ta=(String) course_details.get(2).get(i);
                //System.out.println(tanu);
                int tanum=Integer.parseInt(ta);
                
                String[] preq = pre.split("!");//
                String[] skill = skil.split("!");//
                
                
                
                
                /////courseUtility///////
                for(int s=0;s<totalstudents-1;s++){
                    int indx=course.get(0).indexOf(coursename);
                   // System.out.println(indx);
                    for(int y=0;y<tanum;y++){
                    utility[s][i1+y]=(( Double.parseDouble((String)course.get(s+1).get(indx))) * coursewt);
                   // System.out.println( utility[0][i]);
                }
                 
                }
              //   System.out.println("course"+utility[0][3]);
                
                ///////preUtility////
                 for(int s=0;s<totalstudents-1;s++){
                     int d=preq.length;
                     double util=0;
                     for(int k=0;k<d;k++){
                         int indx1=prereqs.get(0).indexOf(preq[k]);
                        // System.out.println(preq[k]);
                         
                             
                         if(indx1>=0){
                            util= util + Double.parseDouble((String)prereqs.get(s+1).get(indx1));  
                           
                            //System.out.println(util);
                         }
                     }
                      for(int y=0;y<tanum;y++){
                    utility[s][i1+y]= utility[s][i1+y] + (util/d) * preqwt;
                  
                }
                       
                 }
              //  System.out.println("preq"+utility[0][3]);
                
                 ///////skillutility////
                 for(int s=0;s<totalstudents-1;s++){
                     int d=skill.length;
                     double util=0;
                     for(int k=0;k<d;k++){
                         int indx1=skills.get(0).indexOf(skill[k]);
                        
                        if(s==0 && i==1){
                            for(int f=0;f<d;f++){
                                //System.out.println("skill  "+skill[f]);
                            }
                        }
                        
                         if(indx1>=0){
                            util= util + Double.parseDouble((String)skills.get(s+1).get(indx1)); 
                             
                          
                         }
                        
                     }
                      
                     for(int y=0;y<tanum;y++){
                    utility[s][i1+y]= utility[s][i1+y] + (util/d) * skillwt;
                   
                  
                }
                  }
                 
                // System.out.println("skill"+utility[0][3]);
                 
                 
                  /////prefUtility///////
                for(int s=0;s<totalstudents-1;s++){
                    int indx= preferences.get(0).indexOf(coursename);
                   // System.out.println(indx);
                    
                   
                     for(int y=0;y<tanum;y++){
                  utility[s][i1+y]=utility[s][i1+y] + (((1+ Double.parseDouble((String) preferences.get(s+1).get(indx))) * prefwt)*( 1+ (Double.parseDouble((String) shortlist.get(s+1).get(indx))*100)));
                   // System.out.println( utility[0][i]);
                }
                 
                }
               //  System.out.println("pref"+utility[0][3]);
                
                
                
                BufferedWriter br = new BufferedWriter(new FileWriter("utility.csv"));

for(int t=0;t<utility.length;t++){
    StringBuilder sb = new StringBuilder();
for (double element : utility[t]) {
    if(element>-1){
 sb.append(element);
 sb.append(",");
}


}
if(sb.length()>0)
sb.deleteCharAt(sb.length()-1);

br.write(sb.toString());
br.newLine();
}       
 br.close();
 i1=i1+tanum;
 
             }
       // System.out.print("done");
    }
    
    
}

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package taallocation;
import java.io.*;
import java.util.ArrayList; 
import java.util.Arrays;
import java.util.Scanner;
import org.apache.poi.hssf.usermodel.HSSFCell;
import org.apache.poi.hssf.usermodel.HSSFRow;
import org.apache.poi.hssf.usermodel.HSSFSheet;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;



/**
 *
 * @author Khanijau's
 */

public class Ta { 
    ArrayList<int[]> matrix=new ArrayList(); 
    static int[][] data=new int[200][200];
    static int NoOfStu, NoOfCourse;
    static float [][] StuPref = new float [200][199];
    static float [][] CoursePref = new float [199][200];
    static float [][] StuPrefI = new float [200][199];
    static float [][] CoursePrefI = new float [199][200];
    static int [][] SList = new int [200][199];
    static int [][] CList = new int [199][200];
    
    
    public static void read(String file){
        for(int yt1=0; yt1<CList.length;yt1++){
            for(int ty=0;ty<CList[0].length;ty++){
                CList[yt1][ty]=-1;
            }
    
}
        
         for(int yt1=0; yt1<SList.length;yt1++){
            for(int ty=0;ty<SList[0].length;ty++){
                SList[yt1][ty]=-1;
            }
    
}
        
        try{
            BufferedReader bis= new BufferedReader (new FileReader(file)); 
            String input;
            int j=0,k=0;
            NoOfCourse=0;
             input=bis.readLine();
            while((input.length())!=0){
               System.out.println("mn"+input.length());
                if(input.length()!=0)
                {input=input.substring(0, input.length()-1);}   
                
                 System.out.println(input);
               
                String[] s=input.split(","); 
                float[] rows= new float[s.length];
                 System.out.println(s.length);
                if(s.length>NoOfCourse) {
                    NoOfCourse=s.length;
                }
                
                for(int i=0;i<s.length;i++){ 
                    rows[i]=Float.parseFloat(s[i]);
                    StuPref[j][i]=rows[i];
                    CoursePref[i][j]=rows[i];
                    //System.out.print(rows[i]+"\t");
                } 
                //System.out.println();
                j++;
                 System.out.println(j);
                 input=bis.readLine();
            }
            NoOfStu= j;
        }
        catch(IOException | NumberFormatException ex){ 
            System.out.println(ex); 
        }
    }
    
    
    
    
    
    
     public static void writeXLSFile(int list[][],String name,int x,int y) throws IOException {
		int a = 0,ch=0;
               
                               // System.out.println(num);
                String excelFileName;
		
			excelFileName=name;//name of excel file
                
		String sheetName = "Sheet1";//name of sheet
 
		HSSFWorkbook wb = new HSSFWorkbook();
		HSSFSheet sheet = wb.createSheet(sheetName) ;
 
		//iterating r number of rows
                
                for (int r=0;r < x; r++ )
		{
			HSSFRow row = sheet.createRow(r);
			//iterating c number of columns
			for (int c=0;c < y; c++ )
			{
				HSSFCell cell = row.createCell((short) c);
				//int x=list.size();
				
                                    a=list[r][c];
                              if(a!=-1)
				cell.setCellValue(a-1);
				//list.remove(a);
			}
		}//System.out.println("1");
            try (FileOutputStream fileOut = new FileOutputStream(excelFileName)) {
                wb.write(fileOut);
                fileOut.flush();
            }
	}

    public static void createPrefList(){
        int i,j;
        for(i=0;i<NoOfStu;i++) {
            System.arraycopy(StuPref[i], 0, StuPrefI[i], 0, StuPref[i].length);
            Arrays.sort(StuPref[i]);
            for(j=0;j<StuPref[i].length/2;j++){
                float temp = StuPref[i][j];
                StuPref[i][j]=StuPref[i][StuPref[i].length-j-1];
                StuPref[i][StuPref[i].length-j-1]=temp;
            }   
        }
        for(i=0;i<NoOfCourse;i++) {
            System.arraycopy(CoursePref[i], 0, CoursePrefI[i], 0, CoursePref[i].length);
            Arrays.sort(CoursePref[i]);
            for(j=0;j<CoursePref[i].length/2;j++){
                float temp = CoursePref[i][j];
                CoursePref[i][j]=CoursePref[i][CoursePref[i].length-j-1];
                CoursePref[i][CoursePref[i].length-j-1]=temp;
            }
        }
    }
    public static void makeList(){
        int i,j;
        for(i=0;i<NoOfStu;i++) {
            for(j=0;j<NoOfCourse;j++) {
                
                for(int k=0;k<StuPrefI[i].length;k++) {
                        if(Float.compare(StuPref[i][j], StuPrefI[i][k])==0&&StuPrefI[i][k]!=-1){
                            StuPrefI[i][k]=-1;
                            SList[i][j]=k+1;
                            break;
                        }
                }
            }
        }
        System.out.println("/////////////////\n\n\n");
        for(i=0;i<NoOfCourse;i++) {
            for(j=0;j<NoOfStu;j++) {
               
                for(int k=0;k<CoursePrefI[i].length;k++) {
                        if(Float.compare(CoursePref[i][j], CoursePrefI[i][k])==0&&CoursePrefI[i][k]!=-1){
                            CoursePrefI[i][k]=-1;
                            CList[i][j]=k+1;
                            break;
                        }
                }
            }
        }}
    
    public static int[] main() throws IOException{ 
        int[] retrn=new int[2];
        Scanner sc=new Scanner(System.in); 
      
        read("utility.csv");
        
        createPrefList();
        int i,j;
        for(i=0;i<NoOfStu;i++) {
            for(j=0;j<NoOfCourse;j++) {
                System.out.print(StuPref[i][j]+"\t");
            }
            System.out.println();
        }
        System.out.println("/////////////////\n\n\n");
        for(i=0;i<NoOfCourse;i++) {
            for(j=0;j<NoOfStu;j++) {
                System.out.print(CoursePref[i][j]+"\t");
            }
            System.out.println();
        }
        System.out.println("..................");
        for(i=0;i<NoOfStu;i++) {
            for(j=0;j<NoOfCourse;j++) {
                System.out.print(StuPrefI[i][j]+"\t");
            }
            System.out.println();
        }
        System.out.println("/////////////////\n\n\n");
        for(i=0;i<NoOfCourse;i++) {
            for(j=0;j<NoOfStu;j++) {
                System.out.print(CoursePrefI[i][j]+"\t");
            }
            System.out.println();
        }
        makeList();
        System.out.println("**********");
        for(i=0;i<NoOfStu;i++) {
            for(j=0;j<NoOfCourse;j++) {
                System.out.print(SList[i][j]+"\t");
            }
            System.out.println();
        }
        System.out.println("/////////////////\n\n\n");
        for(i=0;i<NoOfCourse;i++) {
            for(j=0;j<NoOfStu;j++) {
                System.out.print(CList[i][j]+"\t");
            }
            
            System.out.println();
        }
         writeXLSFile(CList,"Man.xls",NoOfCourse,NoOfStu);     
   writeXLSFile(SList,"Woman.xls",NoOfStu,NoOfCourse);
        
        /* BufferedWriter br1 = new BufferedWriter(new FileWriter("Man1_1x1.csv"));

for(int t=0;t<CList.length;t++){
    StringBuilder sb1 = new StringBuilder();
for (double element : CList[t]) {
    if(element!=-1){
    
 sb1.append(element-1);
 sb1.append(",");
}}
br1.write(sb1.toString());
br1.newLine();
}       
 br1.close();
 
 
 
  BufferedWriter br2 = new BufferedWriter(new FileWriter("Woman1_1x1.csv"));

for(int t=0;t<SList.length;t++){
    StringBuilder sb2 = new StringBuilder();
for (double element : SList[t]) {
 if(element!=-1){
    sb2.append(element-1);
 sb2.append(",");
}}
br2.write(sb2.toString());
br2.newLine();
}       
 br2.close();
 //System.out.println(NoOfStu+ "   nj");*/
 retrn[0]=NoOfStu;
 retrn[1]=NoOfCourse;
 return retrn;
 
    }
}    
    
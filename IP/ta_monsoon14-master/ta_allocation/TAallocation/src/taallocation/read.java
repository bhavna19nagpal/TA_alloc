package taallocation;



import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Random;

//import javax.swing.text.html.HTMLDocument.Iterator;

import org.apache.poi.hssf.usermodel.HSSFCell;
import org.apache.poi.hssf.usermodel.HSSFRow;
import org.apache.poi.hssf.usermodel.HSSFSheet;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;


public class read {
	
         static int x,y ;
	 static int Man[][];
	 static int Woman[][];
	static int ch=0;

    /**
     *
     * @param i
     */
    public read(int i,int j) {
        x=i;y=j;
        Man=new int[x][y+1];
        Woman=new int[y][x+1];
        }
        
        public static  int [][] readXLSFile(String s) throws IOException
	{
		InputStream ExcelFileToRead;
		int flag=0;
		if(s.equals("Man")){
			System.out.print("manaaa");
                            ExcelFileToRead = new FileInputStream(s+".xls");
                       
                           
		}else{
			ExcelFileToRead = new FileInputStream(s+".xls");
                            
		}
		HSSFWorkbook wb = new HSSFWorkbook(ExcelFileToRead);
 
		HSSFSheet sheet=wb.getSheetAt(0);
		HSSFRow row; 
		HSSFCell cell;
 
		Iterator rows = sheet.rowIterator();
		int i=0,j=0;
		while (rows.hasNext())
		{
			
			row=(HSSFRow) rows.next();
			Iterator cells = row.cellIterator();
			
			while (cells.hasNext())
			{
				cell=(HSSFCell) cells.next();
		
				if (cell.getCellType() == HSSFCell.CELL_TYPE_STRING)
				{
					System.out.print(cell.getStringCellValue()+" ");
				}
				else if(cell.getCellType() == HSSFCell.CELL_TYPE_NUMERIC)
				{     if((int)(cell.getNumericCellValue())>-1){
					if(flag==0){
						Man[i][j]=(int)(cell.getNumericCellValue());
					}else{
						Woman[i][j]=(int)(cell.getNumericCellValue());
					}
					
				}}
				else
				{
					
				}
				j++;
			}
			j=0;
			i++;
			
                      
		}
         if(flag==0){
						return Man;
					}else{
						 return Woman;
					}
	}
	

	public static void display(int[][] t,int x,int y){
		
		for(int i=0;i<x;i++){
			for(int j=0;j<y;j++){
				System.out.print(t[i][j]+" ");
			}
			
			System.out.println();
		}
	}
      public ArrayList<int[][]> main(int a,int b) throws IOException{
		
		Random rand = new Random();
   
                read r=new read(a,b); 
                int f=rand.nextInt(9)+1;
		Man=r.readXLSFile("Man");
                System.out.println("Man - ");
		r.display(Man,x,y);
		System.out.println();
		Woman= r.readXLSFile("Woman");
                
                
		
		
		System.out.println("Woman - ");
		r.display(Woman,y,x);
		System.out.println();
		ArrayList<int[][]> list= new ArrayList<>();
                list.add(Man);
                list.add(Woman);
               
		System.out.println("Result - ");
              
             return list;
}
}
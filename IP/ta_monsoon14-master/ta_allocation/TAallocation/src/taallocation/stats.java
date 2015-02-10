package taallocation;

import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.xy.DefaultXYDataset;
import org.jfree.data.xy.XYDataset;

/**
 *
 * @author sourabh
 */
public class stats {
    
    
     ArrayList<Integer> statW= new ArrayList<>();
          ArrayList<Integer> statM= new ArrayList<>();
          
          ArrayList<Integer> finalStat= new ArrayList<>();
         int men,women;
         double[] sol;
               
          
           double[] data1;
            double[] data2;
            
            proj s;

    
    stats(int m, int n, ArrayList<Object> r){
        this.men=n;
        this.women=n;
         s=(proj) r.get(1);
          sol=(double[]) r.get(0);
       //   sol=r;
           men=m;
           women=n;
         
        
          for(int ko=0;ko<men*women;ko++){
         statW.add(0);
         statM.add(0);
         
     }}

     
      public void graph(){
          
       System.out.println("STATISTICS");
            int me = 0, we = 0;
                    for(int ko=0;ko< men*women;ko++){
                        if(sol[ko]>0.9){
                             me=ko/women;
                             we= ko%women;
                         int x=s.arr.get(me).indexOf(we+1);
                         System.out.println((me+1)+"->"+(we+1));
                      //   x--;
      ////                System.out.println(x);
                          int g=statM.get(x)+1;
                         statM.remove(x);
                          statM.add(x, g);
                        
                        int y=s.arr1.get(we).indexOf(me+1);
                      //  y--;
                        int f=statW.get(y)+1;
                        statW.remove(y);
                        statW.add(y,f);
                        
                        
                        }
                    }
                    
                    
                    
                      System.out.println("STATISTICS");
                    System.out.println(statM);
                      System.out.println(statW);
                      
                      
                      
                       for(int yu=0; yu<men*women;yu++){
                      finalStat.add(yu,statW.get(yu) + statM.get(yu));
                      
                  }
                  System.out.println(finalStat);
                  
                  
                  data1= new double[men+women];
                  for(int t=0; t<(men+women);t++){
                      data1[t]=finalStat.get(t);
                  }
                  
                  data2= new double[statW.size()];
                  for(int t=0; t<statW.size();t++){
                      data2[t]=statW.get(t);
                  }}
                  
                      
     
        
           
      public  XYDataset createDataset() {
 
        DefaultXYDataset ds = new DefaultXYDataset();
                double[] data11=new double[men+women];
                System.out.println(men+women);
                for(int t=0;t<(men+women);t++){
                    data11[t]=t+1;
                }
        
 
        double[][] data = { data11 , data1 };
 
        ds.addSeries("series1", data);
 
        return ds;
    }
    
      
            
 
}

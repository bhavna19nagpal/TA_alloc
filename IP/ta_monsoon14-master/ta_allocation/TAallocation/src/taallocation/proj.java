/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package taallocation;
//// remove coment with for 4 slashes for previous version with print 

import java.util.ArrayList;

/**
 *
 * @author sourabh
 */
public class proj {

    /**
     * @param args the command line arguments
     */
   
     ArrayList<ArrayList> arr=new ArrayList<>();
      ArrayList<ArrayList> arr1=new ArrayList<>();
       ArrayList<double[]> const1=new ArrayList<>();
      ArrayList<double[]> const2=new ArrayList<>();
      
       int[][] TWOd;
        int count=0;
    
    
    public proj(int m, int w){
      TWOd = new int[m*w][m*w];
        for(int k=0;k<m;k++){
            for(int r=0;r<w;r++){
                TWOd[k][r]=0;
            }}    
    }
    
    
    
    
    
        
        
        public int addmen(int[] pref){
             ArrayList<Integer> men=new ArrayList<>();
         int s=pref.length;
         for(int u=0;u<s;u++){
         men.add(pref[u]);
         }
           arr.add(men); 
            return 0;
        }
    
    
        public int addwomen(int[] pref){
             ArrayList<Integer> women=new ArrayList<>();
             int s=pref.length;
         for(int u=0;u<s;u++){
         women.add(pref[u]);
         }
          arr1.add(women);
        return 0;    
        }
       
        
        public int allocate(int n1, int n2){
        
         int size=(arr.size());
        //// System.out.print(size);
      
        // size=2;
       for(int i=0;i<size;i++){
      //  int i=2;
        
       
         int size2=arr1.size();
          // size2=1;
         
         
         for(int j=0;j<size2;j++){
               int[] x = new int[n1*n2];
               for(int po=0;po<(n1*n2);po++){
                   x[po]=0;
               }
        
               
           x[(i*n2)+j]=1;
        //System.out.print("\nsourabh");
        int index=arr.get(i).indexOf(j+1);
    //    System.out.print("\n 1:");
      //  System.out.print(index);
        for(int ind=0;ind<index;ind++){
           int ind1= (int) arr.get(i).get(ind);
           x[(i*n2)+(ind1-1)]=1;
        //System.out.print("\nsingh");
        }
           
         int index1=arr1.get(j).indexOf(i+1);
           
          //   System.out.print("\n 2:");
        //System.out.print(index1);
           for(int ind2=0;ind2<index1;ind2++){
               
               int ind3= (int) arr1.get(j).get(ind2);
          //       System.out.print("\n 3:");
        //System.out.print(ind3);
               int f= (ind3-1)*n2+j;
              /* System.out.println(f);
                System.out.println("LOLLOLLOL");
                System.out.println(ind3);
                 System.out.println(n2);
                  System.out.println(j);
               */
               
               x[(ind3-1)*n2+j]=1;
               
              
           }
         TWOd[count]=x;   
         count++;   
         
   }
        
        
        
  }   
    System.out.print("\n");
    
    for(int kl = 0; kl<=TWOd.length-1; kl++ ) {
        ////System.out.println();
        for(int lk=0;lk<TWOd[kl].length;lk++){
       //// System.out.print(TWOd[kl][lk]);
        }  }
    
  
        return 0;
        }
        
        public int constrain1(int n1, int n2){
            for(int op=0;op<n1;op++){
                double[] arry= new double[n1*n2];
                 for(int ko=0;ko<n1*n2;ko++){
                     arry[ko]=0.0;
                 }
                 for(int pl=0;pl<n2;pl++){
                     arry[(op*n2)+pl]=1.0;   
                 }
            
            const1.add(arry);
            
            
           // System.out.println(arry);
            }
            for(int ol=0;ol<n1;ol++){
             for(int lo=0;lo<n2*n1;lo++){
             ////System.out.print(const1.get(ol)[lo]);
            }
          ////  System.out.println();
            }
           return 0; 
        }
        
        
        
        public int constrain2(int n1, int n2){
             for(int op=0;op<n2;op++){
                double[] arry= new double[n1*n2];
                 for(int ko=0;ko<n1*n2;ko++){
                     arry[ko]=0.0;
                 }
                 for(int pl=0;pl<n1;pl++){
                     arry[op+(n2*pl)]=1.0;   
                 }
             
                 const2.add(arry);
                
             }
              for(int ol=0;ol<n2;ol++){
             for(int lo=0;lo<n2*n1;lo++){
          ////   System.out.print(const2.get(ol)[lo]);
            }
         ////   System.out.println();
            }
             // System.out.println(const2.size());
            return 0;
        }
        
        
        
        
        public double[] emptyar(int n1, int n2){
             double[] linear= new double[n1*n2];
              
              for(int re=0;re<n1*n2;re++){
                  linear[re]=0.0;
              }
              
              return linear;
        }
        
        
      public double[] int2double(int[] numbers){
     double[] newNumbers = new double[numbers.length];
for (int index = 0; index < numbers.length; index++)
newNumbers[index] = (double)numbers[index];

return newNumbers; 
}       
      
      
      public double[] list2double(ArrayList<Integer> integers){
          double[] ret = new double[integers.size()];
    for (int i=0; i < ret.length; i++)
    {
        ret[i] = integers.get(i).intValue();
    }
    return ret;    
      }
      
      
      
    
            
        }


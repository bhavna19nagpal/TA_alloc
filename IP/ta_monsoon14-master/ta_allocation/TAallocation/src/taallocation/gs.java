package taallocation;




import java.util.*;

public class gs
{
    // Number of men (=number of women)
    private int n,n1 ;
    public static int ch=0;
    // Preference tables (size nxn)
    private int[][] man;
    private int[][] woman;
    public static int rt;

   // private static final boolean d = false;
    private Random rand = new Random();

    /**
     * Creates and solves a random stable marriage problem of
     * size n, where n is given on the command line.
     */
    public int[] imp(int x,int y,int mn[][],int wn[][]) {
	
if (x>y){
    ch=1;
}
	gs sm = new gs(x,y,mn,wn);

	    //sm.printp();
	int[] mr = sm.stable();

	    sm.printm(mr);
            return mr;
    }

    /**
     * Creates a marriage problem of size n with random preferences.
     */
    public gs(int n,int n1,int mn[][],int wn[][]) {
        super();
	//System.out.print(ch+"aa");
        if (ch==0){
        this.n = n;
        this.n1=n1;
        man = new int[n][n1];
	woman = new int[n1][n];
        man=mn.clone();
        woman=wn.clone();
        }
        else
        {
        this.n = n1;
        this.n1=n;
        man = new int[n1][n];
	woman = new int[n][n1];
        man=wn.clone();
        woman=mn.clone();
        }
	/*for (int i = 0; i < n; i++) {
	    man[i] = new int[n];
	    create(man[i]);
	    woman[i] = new int[n];
	    create(woman[i]);
	}*/
    }

    private void create(int[] v) {
	// Create a vector with the values 0, 1, 2, ...
	for (int i = 0; i < v.length; i++)
	    v[i] = i;
	// Create a random permutation of this vector.
	for (int i = v.length - 1; i > 0; i--) {
	    // swap v[i] with a random element v[j], j <= i.
	    int j = rand.nextInt(i+1);

            int temp = v[i];
	    v[i] = v[j];
	    v[j] = temp;
	}
    }

        public int[] stable() {
	// Indicates that woman i is currently engaged to
	// the man v[i].
	int[] current = new int[n1];
	final int not_eng = -1;
	for (int i = 0; i < current.length; i++)
	    current[i] = not_eng;
        
	// List of men that are not currently engaged.
	LinkedList<Integer> freemen = new LinkedList<Integer>();
	for (int i = 0; i < n; i++)
	    freemen.add(i);

	// next[i] is the next woman to whom i has not yet proposed.
	int[] next = new int[n1];

	//computeRanking();
	while (!freemen.isEmpty()) {
            
	    int m = freemen.remove();
	    int w = man[m][next[m]];
	    next[m]++;
	//  System.out.print("m=" + m + " w=" + w+freemen.toString()+"\n"+current[w]);
	    if (current[w] == not_eng) {
		current[w] = m;
	    } else {
		int m1 = current[w];
		if (prefers(w, m, m1)) {
		    current[w] = m;
		    freemen.add(m1);
		} else {
		    freemen.add(m);
		}
	    }	    
	}
	return current;	
    }

    /**
     * Returns true if w prefers x to y.
     */
    private boolean prefers(int w, int x, int y) {
	for (int i = 0; i < n; i++) {
	    int pref = woman[w][i];
	    if (pref == x)
		return true;
	    if (pref == y)
		return false;	    
	}
	// This should never happen.
	System.out.println("Error in womanPref list " + w);
	return false;
    }

    public void printp() {
	System.out.println("manPref:");
	printl(man);
	System.out.println("womanPref:");
	printl(woman);
    }

    private void printm(int[] m) {
	int count=0;
        System.out.println("Married couples (woman + man): ");
	for (int i = 0; i < m.length; i++){
        if(m[i]<0)
            count++;       
        else {if (ch==1)    System.out.println(m[i] + " -> " + i);
        else System.out.println(i + " -> " + m[i]);
    }}
    }
 /*   private void printd(String s) {
	if (DEBUGGING) {
	    System.out.println(s);
	}
    }

         */
    private void printl(int[][] v) {
	if (v == null) {
	    System.out.println("<null>");
	    return;
	}
	for (int i = 0; i < v.length; i++) {
	    for (int j = 0; j < v[i].length; j++)
		System.out.print(v[i][j] + " ");
	    System.out.println();
	}
    }
}
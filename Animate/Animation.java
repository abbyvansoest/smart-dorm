import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

import javax.imageio.ImageIO;
import java.awt.image.*;

public class Animation {

	public static String get_filename(int index) {

		    if (index == 1) return "tuesday_first";
		    if (index == 2) return "tuesday_second";
		    if (index == 3) return "tuesday_third";
		    if (index == 4) return "weds_first";
		    if (index == 5) return "weds_second";
		    if (index == 6) return "weds_third";
		    if (index == 7) return "thurs_first";
		    if (index == 8) return "thurs_second";
		    if (index == 9) return "thurs_third";
		    if (index == 10) return "friday_first";
		    if (index == 11) return "friday_second";
		    if (index == 12) return "friday_third";
		    if (index == 13) return "saturday_first";
		    if (index == 14) return "saturday_second";
		    if (index == 15) return "saturday_third";
		    if (index == 16) return "sunday_first";
		    if (index == 17) return "sunday_second";
		    if (index == 18) return "sunday_third";
		    if (index == 19) return "monday_first";
		    if (index == 20) return "monday_second";
		    if (index == 21) return "monday_third";

		    return "ERROR/NOPE";

	}

	public static String toString(double[][] M) {
	    String separator = ", ";
	    StringBuffer result = new StringBuffer();

	    // iterate over the first dimension
	    for (int i = 0; i < M.length; i++) {
	        // iterate over the second dimension
	        for(int j = 0; j < M[i].length; j++){
	            result.append(M[i][j]);
	            result.append(separator);
	        }
	        // remove the last separator
	        result.setLength(result.length() - separator.length());
	        // add a line break.
	        result.append("\n");
	    }
	    return result.toString();
	}


	public static double[][] get_coords(String floor, int width, int height) {

		double w = (double)width;
		double h = (double)height;

		if (floor.equals("first")) {
			double[][] array = {{220/w, (h-198)/h},{276/w, (h-124)/h}, {250/w, (h-400)/h},{218/w, (h-260)/h},{290/w,(h-184)/h},{150/w,(h-350)/h}};
			return array;
		}

		if (floor.equals("second")) {
			double[][] array = {{204/w, (h-343)/h},{204/w, (h-224)/h}, {295/w, (h-354)/h},{390/w, (h-364)/h},{608/w,(h-400)/h},{85/w,(h-390)/h}};
			return array;
		}

		if (floor.equals("third")) {
			double[][] array = {{200/w, (h-140)/h},{224/w, (h-360)/h}, {240/w, (h-240)/h},{330/w, (h-380)/h},{436/w,(h-395)/h},{116/w,(h-416)/h}};
			return array;
		}
		else {
			System.out.println("Not a Floor!");
			double[][] ret_arr = new double[1][1];
			return ret_arr;
		}
	}

	public static String get_time(int track) {

		String hour = Integer.toString(track/60);
		String min = Integer.toString(track%60);

		if (hour.length() != 2) {
			if (hour.length() < 2) {
				hour = "0"+hour;
			}
			if (hour.length() > 2) {
				return "WRONG";
			}
		}
		if (min.length() != 2) {
			if (min.length() < 2) {
				min = "0"+min;
			}
			if (min.length() > 2) {
				return "WRONG";
			}
		}

		return hour+":"+min;

	}

	public static void main(String[] args) {

		try {

			String day = args[0];
			String floor = args[1];
			String filename = "animate_data/global_"+day+"_"+floor+".txt";
			System.out.println(filename);

			String floorplan = "";
			if (floor.equals("first")) {
				floorplan = "Bloomberg1.png";
			}
			else if (floor.equals("second")) {
				floorplan = "Bloomberg2.png";
			}
			else if (floor.equals("third")) {
				floorplan = "Bloomberg3.png";
				System.out.println("third floor");
			}
			else {
				System.out.println("No plan for that floor!");
			}

			// load floor image
			BufferedImage img = null;
			try {
			    img = ImageIO.read(new File(floorplan)); // eventually C:\\ImageTest\\pic2.jpg
			} 
			catch (IOException e) {
			    e.printStackTrace();
			}

			int width = img.getWidth();
			int height = img.getHeight();

			StdDraw.setCanvasSize(width, height);
			StdDraw.picture(0.5, 0.5, floorplan);
			//StdDraw.setPenColor(StdDraw.YELLOW);
			//StdDraw.filledCircle(.25, .25, .025);

			double[][] coords = get_coords(floor, width, height);
			//System.out.println(toString(coords));

			// Open the file
			BufferedReader br = new BufferedReader(new FileReader(filename));
		    String line;

		    double r = .025;

		    //  Animate the day
		    int tracker = 0;
		    boolean[] justOff = new boolean[6];
		    while ((line = br.readLine()) != null) {

		       // process each minute
		    	String[] active_array = line.split("\t");
		    	for (int i = 0; i < 6; i++) {
		    		//System.out.println(i);
		    		double x = coords[i][0];
		    		double y = coords[i][1];

		    		StdDraw.filledCircle(x,y,r);
		    		
		    		if (active_array[i].equals("1")) {
		    			StdDraw.setPenColor(StdDraw.RED);
		    			StdDraw.filledCircle(x, y, r);
		    			StdDraw.setPenColor(StdDraw.BLACK);
		    		}
		    	}

		    	String prev_time = get_time(tracker-1);
		    	StdDraw.setPenColor(StdDraw.WHITE);
		    	StdDraw.text(.8,.8,prev_time);

		    	String time = get_time(tracker);
		    	StdDraw.setPenColor(StdDraw.BLACK);
		    	StdDraw.text(.8,.8,time);

		    	StdDraw.show();
		    	StdDraw.pause(100);
		    	tracker++;
		    }

			// close input stream
			br.close();
		}

		catch (IOException e)
        {
            System.out.println("File I/O error!");
        }
	}
}



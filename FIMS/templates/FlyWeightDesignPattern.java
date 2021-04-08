public class FlyWeightDesignPattern 
 { 
    private static final String[] colors = {"Red","Orange","Blue","Yellow","Pink"}; 
    public static void main(String[] args)  
    { 
        for(int i=0;i<20;i++) 
        { 
            int rand = (int)(Math.random()*colors.length); 
            Bird bird = BirdFactory.getAngryBird(colors[rand]); 
            bird.draw(); 
        } 
    } 
     
} 
 
 
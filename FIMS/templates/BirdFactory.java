import java.util.HashMap; 
 
public class BirdFactory  
{ 
    private static final HashMap birdMap = new HashMap(); 
     
   public static AngryBird getAngryBird(String colour) 
    { 
         AngryBird abird = (AngryBird) birdMap.get(colour); 
         if(abird == null) 
         { 
            abird = new AngryBird(colour); 
            birdMap.put(colour,abird); 
            System.out.println("Creating Angry Bird of Colour:"+colour); 
         } 
        return abird; 
    } 
}
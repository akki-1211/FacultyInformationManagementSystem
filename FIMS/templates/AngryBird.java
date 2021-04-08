public class AngryBird implements Bird {
    private Color color = null;
    AngryBird(String name)
    {
        color = new Color(name);
    }
    @Override 
    public void draw() 
    { 
        System.out.println("Drawing a Bird of Colour: "+color.getName()); 
    } 
}

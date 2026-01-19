import java.awt.FlowLayout; 
 
import javax.swing.ImageIcon; 
import javax.swing.JFrame; 
import javax.swing.JLabel; 
 
public class Image extends JFrame { 
 private ImageIcon image1; 
 private JLabel label1; 
 private ImageIcon image2; 
 private JLabel label2; 
  
 Image(){ 
  setLayout(new FlowLayout()); 
  image1 = new ImageIcon(getClass().getResource("ice.jpg")); 
  label1 = new JLabel(image1); 
  add(label1); 
   
  image2 = new ImageIcon(getClass().getResource("pust.png")); 
  label2 = new JLabel(image2); 
  add(label2); 
   
 } 
  
 public static void main(String args[]) { 
   
  Image gui = new Image(); 
  gui.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); 
  gui.setVisible(true); 
  gui.pack(); 
  gui.setTitle("Image Program"); 
 } 
 
} 
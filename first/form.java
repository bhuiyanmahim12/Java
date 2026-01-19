import java.awt.event.ActionEvent; 
import java.awt.event.ActionListener; 
import javax.swing.JButton; 
import javax.swing.JFrame; 
import javax.swing.JLabel; 
import javax.swing.JPanel; 
import javax.swing.JTextField; 

public class form implements ActionListener { 
    private static JLabel success; 
    private static JFrame frame; 
    private static JLabel label1, label2, label3; 
    private static JPanel panel; 
    private static JButton button; 
    private static JTextField userText1, userText2, userText3; 
    
    public static void main(String[] args) { 
        frame = new JFrame(); 
        panel = new JPanel(); 
        frame.setSize(400, 300); 
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); 
        frame.add(panel); 
        panel.setLayout(null); 
        
        // Setting all Three Labels 
        label1 = new JLabel("Name"); 
        label1.setBounds(10, 10, 80, 25); 
        panel.add(label1); 
        
        label2 = new JLabel("Roll"); 
        label2.setBounds(10, 60, 80, 25); 
        panel.add(label2); 
        
        label3 = new JLabel("Department"); 
        label3.setBounds(10, 110, 80, 25); 
        panel.add(label3); 
        
        // Creating all TextFields 
        userText1 = new JTextField("Enter Your Name"); 
        userText1.setBounds(100, 10, 200, 25); 
        panel.add(userText1); 
        
        userText2 = new JTextField("Enter Your Roll"); 
        userText2.setBounds(100, 60, 200, 25); 
        panel.add(userText2); 
        
        userText3 = new JTextField("Enter Your Department"); 
        userText3.setBounds(100, 110, 200, 25); 
        panel.add(userText3); 
        
        button = new JButton("Save"); 
        button.setBounds(150, 160, 80, 25); 
        button.addActionListener(new form()); 
        panel.add(button); 
        
        success = new JLabel(""); 
        success.setBounds(130, 210, 300, 25); 
        panel.add(success); 
        
        frame.setVisible(true); 
    } 
    
    @Override 
    public void actionPerformed(ActionEvent e) { 
        String name = userText1.getText();
        String roll = userText2.getText();
        String dept = userText3.getText();
        success.setText("Saved: " + name + ", " + roll + ", " + dept); 
    } 
}
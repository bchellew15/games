/**
	Blake Chellew
	Tower Defense (Java Version)
*/

//eventually can create a game class


//graphics imports
import acm.program.*;
import acm.util.*;
import acm.graphics.*;

//imports for mouse clicks and color
import java.awt.event.*;
import java.awt.Color;

//import for text input
import java.util.Scanner;

//shape imports
import acm.graphics.GOval;
import acm.graphics.GRect;
import acm.graphics.GPolygon;
import acm.graphics.GLabel;
import acm.graphics.GTurtle;

//sound imports
import javax.sound.sampled.*;
import java.io.File;
import java.applet.Applet;
import java.applet.AudioClip;
import java.net.MalformedURLException;
import java.net.URL;


public class TowerDefense extends GraphicsProgram
{
	//Set the size of the window:
	public static final int APPLICATION_WIDTH = 700; 
	public static final int APPLICATION_HEIGHT = 700;
	
	public static int health = 100;
	
	static EnemyBullet[] enemyFleet;
	static PlayerBullet[] playerFleet;
	
	static int enemyNumber = 20;
	static int playerNumber = 20;
	
	public static void takeDamage() {
		health--;
	}
	
	public void mousePressed(MouseEvent e) {
		int index = 0;
		PlayerBullet temp = playerFleet[0];
		
		while( temp.isActive && index < playerNumber - 1 ) {
			index++;
			temp = playerFleet[index];
		}
				
		if( temp.isActive == false )
			temp.activate( e.getX(), e.getY() );
	}
	
	public void run()
	{		
		//create the background
		GRect backSquare = new GRect( 0, 0, 1000, 1000 );
		add( backSquare );
		backSquare.setFilled(true);
		backSquare.setColor(Color.LIGHT_GRAY);
		
		//create the center square
		GRect centerSquare = new GRect( 315, 315, 70, 70 );
		add( centerSquare );
		centerSquare.setFilled(true);
		centerSquare.setColor(Color.BLACK);
		
		//Create the health indicator
		GLabel healthLabel = new GLabel("Health: " + health, 10, 20);
		add( healthLabel );
		healthLabel.setVisible(true);
		
		enemyFleet = new EnemyBullet[enemyNumber];
		for( int i = 0; i < enemyNumber; i++ )
		{
			enemyFleet[i] = new EnemyBullet();
			enemyFleet[i].addTo(this);
		}
		
		playerFleet = new PlayerBullet[playerNumber];
		for( int i = 0; i < playerNumber; i++ )
		{
			playerFleet[i] = new PlayerBullet();
			playerFleet[i].addTo(this);
		}
		
		int counter = 0;
		
		addMouseListeners(); //enables mouse reception
		
		while( health > 0 )//change back to 0
		{
			if( counter % 40 == 0 )//enemy interval
			{
				int index = 0;
				EnemyBullet temp = enemyFleet[0];
				
				while( temp.isActive && index < enemyNumber - 1 )
				{
					index++;
					temp = enemyFleet[index];
				}
				
				if( temp.isActive == false )
				{
					temp.activate();
				}
				
			}
				
			//call the move method on active enemy bullets
			for( int i = 0; i < enemyNumber; i++ )
			{
				if( enemyFleet[i].isActive )
					enemyFleet[i].move();
			}
			
			//call the move method on active player bullets
			for( int i = 0; i < playerNumber; i++ )
			{
				if( playerFleet[i].isActive )
					playerFleet[i].move();
			}
			
			//refresh health
			healthLabel.setVisible(false);
			healthLabel = new GLabel("Health: " + health, 10, 20);
			add(healthLabel);
			
			pause(80);//animation speed
			counter++;
		}
		
		//Display Label, "you lose"
		pause(500);
		System.exit(0);
	}
	
	//extra stuff to play sound
	public static AudioClip getAudioClip( String relativeURL ) {
		URL completeURL = null;
		try {
			URL baseURL = new URL("file:" + System.getProperty("user.dir") + "/");		
			completeURL = new URL(baseURL, relativeURL);
			System.out.println( "Accessing: " + completeURL.toString() );
		} catch (MalformedURLException e){
			System.err.println(e.getMessage());
		} catch( Exception e) {
			
		}
		AudioClip audioClip = Applet.newAudioClip(completeURL);
		return audioClip;				
	}
		
	public static void main(String[] args)
	{
		new TowerDefense().start(args);
	} 
}

class EnemyBullet
{
	public GOval o;
	public boolean isActive = false;
	public double startX = -30;
	public double startY = -30;
	
	public EnemyBullet()
	{
		o = new GOval( 10, 10 ); 
		o.setFilled(true);
		o.setColor(Color.RED);
	}
	
	public void activate()
	{
		isActive = true;
		double degrees = Math.random() * 360;
		startX = 1000 * Math.sin(degrees);
		startY = 1000 * Math.cos(degrees);
		o.setLocation(startX, startY);
		//This is where the initial position should be set
	}
	
	public void deActivate()
	{
		isActive = false;
	}
	
	public void move()
	{
		double rise = (350 - startY) / 500;
		double run = (350 - startX) / 500;
		
		//move based on the starting position, should be set randomly at activation
		//here moves in straight line, will eventually curve
		
		o.move( run, rise );
		
		//check if it hits a player bullet:
		for( int i = 0; i < TowerDefense.playerNumber; i++ )
			if( TowerDefense.playerFleet[i].isActive )
				if( o.getX() - TowerDefense.playerFleet[i].o.getX() < 10 && o.getX() - TowerDefense.playerFleet[i].o.getX() > -10 && o.getY() - TowerDefense.playerFleet[i].o.getY() < 10 && o.getY() - TowerDefense.playerFleet[i].o.getY() > -10  )
				{
					//play sound:
					AudioClip clip = TowerDefense.getAudioClip("ExplosionSound.wav");//insert wav file
					clip.play();
					
					//deactivate bullets:
					deActivate();
					TowerDefense.playerFleet[i].deActivate();					
				}			
		
		//if it hits the target, deactivate and decrease health
		if( o.getX() - 315 < 70 && o.getX() - 315 > -10 && o.getY() - 315 < 70 && o.getY() - 315 > -10 )
		{
			//play sound:
			AudioClip clip = TowerDefense.getAudioClip("ExplosionSound.wav");//insert wav file
			clip.play();
			
			//The center box takes damage:
			deActivate();
			TowerDefense.takeDamage();
		}
	}
		
	public void addTo (GraphicsProgram gr)
	{
		gr.add(o);
	}
}

class PlayerBullet
{
	public GOval o;
	public boolean isActive = false;
	private double mouseX;
	private double mouseY;
	
	public PlayerBullet()
	{
		o = new GOval( -30, -30, 10, 10 ); 
		o.setFilled(true);
		o.setColor(Color.BLUE);
	}
	
	public void activate( double mouseX, double mouseY)
	{
		isActive = true;
		o.setLocation(350, 350);
		this.mouseX = mouseX;
		this.mouseY = mouseY;
	}
	
	public void deActivate()
	{
		isActive = false;
		o.setLocation(-30, -30);
	}
	
	public void move()
	{
		double rise = (mouseY - 350) / 10;
		double run = (mouseX - 350) / 10;
		o.move( run, rise );
		//moves away from the center based on the mouse location
		
		//if hits edge of screen, deactivate
		if( o.getX() < -10 || o.getX() > 700 || o.getY() < -10 || o.getY() > 700 )
			deActivate();
		
		//code for deactivation is already in the enemies
	}
	
	public void addTo (GraphicsProgram gr)
	{
		gr.add(o);
	}
}
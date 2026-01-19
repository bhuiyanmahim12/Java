class sus_res_stop implements Runnable
{
    Thread th;
    boolean suspend_flag, stop_flag;

    sus_res_stop(String name)
    {
        th = new Thread(this, name);
        suspend_flag = false;
        stop_flag = false;
        th.start();
    }

    public void run()
    {
        try
        {
            int j = 1;
            while (j++ < 20)
            {
                synchronized (this)
                {
                    while (suspend_flag)
                        wait();

                    if (stop_flag)
                        break;
                }
            }
        }
        catch (InterruptedException e)
        {
            System.out.println("Thread interrupted");
        }
    }

    synchronized void my_suspend()
    {
        suspend_flag = true;
    }

    synchronized void my_resume()
    {
        suspend_flag = false;
        notify();
    }

    synchronized void my_stop()
    {
        suspend_flag = false;
        stop_flag = true;
        notify();
    }
}

public class eg_SRS
{
    public static void main(String args[])
    {
        try
        {
            sus_res_stop S_R_S_T = new sus_res_stop("SRS");

            System.out.println("Thread S_R_S_T is created and started");
            Thread.sleep(2000);

            S_R_S_T.my_suspend();
            System.out.println("Thread S_R_S_T is suspended");
            Thread.sleep(2000);

            S_R_S_T.my_resume();
            System.out.println("Thread S_R_S_T is resumed");
            Thread.sleep(2000);

            S_R_S_T.my_stop();
            System.out.println("Thread S_R_S_T is stopped");
        }
        catch (InterruptedException e)
        {
            System.out.println("Generated interrupted exception");
        }
    }
}

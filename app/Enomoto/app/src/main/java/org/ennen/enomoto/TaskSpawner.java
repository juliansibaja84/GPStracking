package org.ennen.enomoto;

import android.util.Log;

import java.util.ArrayList;
import java.util.concurrent.Executor;

/**
 * Created by asmateus on 15/10/16.
 */

public class TaskSpawner implements Executor
{
    ArrayList<Task> tasks = new ArrayList<>();

    @Override
    public void execute(Runnable r)
    {
        Log.d("tasking", "CREATING NEW TASK");
        new Thread(r).start();
    }

    public void createTask(int task_id)
    {
        int i = 0;
        if(this.tasks.isEmpty()) {
            tasks.add(new Task(task_id));
            execute(tasks.get(tasks.size() - 1));
        }
        else {
            while(i < this.tasks.size() && this.tasks.get(i).task_id != task_id) ++i;
            if(i == this.tasks.size()) {
                tasks.add(new Task(task_id));
                execute(tasks.get(tasks.size() - 1));
            }
        }
    }

    public void deleteTask(int task_id)
    {
        int i = 0;
        while(i < this.tasks.size() && this.tasks.get(i).task_id != task_id) ++i;
        if(i != this.tasks.size()) {
            this.tasks.get(i).stop();
            this.tasks.remove(i);
        }
    }

    private class Task implements Runnable
    {
        private boolean shutdown = false;
        public int task_id;

        public Task(int task_id)
        {
            this.task_id = task_id;
        }

        @Override
        public void run()
        {
            while(!shutdown) {

                try {
                    Log.d("tasking2", "HELLO FROM TASK " + task_id);
                    Thread.sleep(3000);
                }
                catch (Exception e) {}
            }
        }

        public void stop()
        {
            this.shutdown = true;
        }
    }
}

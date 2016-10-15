package org.ennen.enomoto;

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
        this.execute(r);
    }

    public void createTask(int task_id)
    {
        int i = 0;
        while(this.tasks.get(i).task_id != task_id && i < this.tasks.size()) ++i;
        if(this.tasks.get(i).task_id != task_id) {
            tasks.add(new Task(task_id));
            execute(tasks.get(tasks.size() - 1));
        }
    }

    public void deleteTask(int task_id)
    {
        int i = 0;
        while(this.tasks.get(i).task_id != task_id && i < this.tasks.size()) ++i;
        if(this.tasks.get(i).task_id == task_id) {
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

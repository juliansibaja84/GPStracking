package org.ennen.enomoto;

/**
 * Created by asmateus on 14/10/16.
 */

import android.os.AsyncTask;
import android.util.Log;
import android.widget.Toast;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.*;
import java.util.concurrent.Executor;

public class ServerConnector implements Executor {

    private URL url;
    private final String USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11";

    public ServerConnector(String url, int port, MainActivity master)
    {
        try {
            this.url = new URL("http", url, port, "/historic/stats/");
        }
        catch (MalformedURLException e) {
            Log.d("connection_error", e.toString());
        }

        this.execute(new ServerUpdater(this.url, master));
    }

    public boolean connectionStatus()
    {
        // Send test data to server and verify response integrity
        return true;
    }

    @Override
    public void execute(Runnable r) {
        new Thread(r).start();
    }

    class ServerUpdater implements Runnable {
        private URL url;
        private MainActivity master;
        private String data_pop;

        public ServerUpdater(URL url, MainActivity master)
        {
            this.url = url;
            this.master = master;
        }

        @Override
        public void run()
        {
            while(true) {
                if(!master.collected_info_stack.empty()) {
                    data_pop = master.collected_info_stack.pop();
                    try {
                        post(data_pop);
                    } catch (Exception e) {

                        // Undo stack pop;
                        master.collected_info_stack.push(data_pop);
                        Log.d("Conn_ex", "Error connecting " + e.toString());
                    }
                }
                else {
                    Log.d("stack_empty", "Stack empty, nothing to do");
                }

                // Timeout of 2 seconds
                try {
                    Thread.sleep(2000);
                } catch(InterruptedException ex) {
                    Thread.currentThread().interrupt();
                }
            }
        }

        // Data is a string which values are separated by @
        public void post(String data) throws Exception
        {
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("User-Agent", USER_AGENT);

            //String urlParameters = "sn=C02G8416DRJM&cn=&locale=&caller=&num=12345";

            // Send post request
            conn.setDoOutput(true);
            DataOutputStream wr = new DataOutputStream(conn.getOutputStream());
            wr.writeBytes(data);
            wr.flush();
            wr.close();

            int responseCode = conn.getResponseCode();
            Log.d("URL", "Sending 'POST' request to URL : " + url);
            Log.d("Post_param", "Post parameters : " + data);
            Log.d("response_code", "Response Code : " + responseCode);

            if(responseCode == 200) {
                master.server_conn_status = true;
            }
            else {
                master.server_conn_status = false;
            }

            BufferedReader in = new BufferedReader(
                    new InputStreamReader(conn.getInputStream()));
            String inputLine;
            StringBuffer response = new StringBuffer();

            while ((inputLine = in.readLine()) != null) {
                response.append(inputLine);
            }
            in.close();

            //print result
            Log.d("response", response.toString());
        }
    }
}

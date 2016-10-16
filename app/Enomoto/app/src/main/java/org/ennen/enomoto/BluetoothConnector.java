package org.ennen.enomoto;

import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.DialogInterface;
import android.content.Intent;
import android.util.Log;
import android.widget.Toast;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Set;
import java.util.UUID;

/**
 * Created by asmateus on 15/10/16.
 */

public class BluetoothConnector
{
    private static final int REQUEST_ENABLE_BT = 1;
    private ArrayList<String> paired_adapter_list = new ArrayList<>();
    private BluetoothAdapter mBlAdapter;
    private MainActivity master;
    private ConnectThread conn_t = null;

    public boolean conn_status = false;
    public String selected_device_MAC = "";

    public BluetoothConnector(MainActivity master)
    {
        this.master = master;
        this.mBlAdapter = BluetoothAdapter.getDefaultAdapter();
        if (mBlAdapter == null) {
            Toast toast = Toast.makeText(master.getApplicationContext(), "Bluetooth not Supported", Toast.LENGTH_LONG);
            toast.show();
        }
        else {
            if (!this.mBlAdapter.isEnabled()) {
                Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                master.startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
            }
            else {
                searchPairedDevices();
            }
        }
    }

    public boolean blStatus()
    {
        return (this.mBlAdapter != null && this.mBlAdapter.getBondedDevices().size() > 0);
    }

    private void connectThroughMAC()
    {
        if(this.selected_device_MAC != "") {
            Log.d("Address", this.selected_device_MAC);
            conn_t = new ConnectThread(this.mBlAdapter.getRemoteDevice(this.selected_device_MAC));
            conn_t.start();
        }
    }

    private void searchPairedDevices()
    {
        Set<BluetoothDevice> pairedDevices = this.mBlAdapter.getBondedDevices();
        // If there are paired devices
        if (pairedDevices.size() > 0) {
            // Loop through paired devices
            for (BluetoothDevice device : pairedDevices) {
                // Add the name and address to an array adapter to show in a ListView
                paired_adapter_list.add(device.getName() + "\n" + device.getAddress());
            }
            buildSelectDialog();
        }
        else {
            Toast toast = Toast.makeText(master.getApplicationContext(), "Please pair with your OBD-II Adapter and try again", Toast.LENGTH_LONG);
            toast.show();
        }
    }

    private void buildSelectDialog()
    {
        AlertDialog.Builder builder = new AlertDialog.Builder(master);
        builder.setTitle("Select Adapter");
        builder.setItems(
                this.paired_adapter_list.toArray(new CharSequence[this.paired_adapter_list.size()]),
                new DialogInterface.OnClickListener()
                {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        selected_device_MAC = paired_adapter_list.get(which).split("\n")[1];
                        Toast toast = Toast.makeText(master.getApplicationContext(), "Selected " + selected_device_MAC, Toast.LENGTH_LONG);
                        toast.show();
                        connectThroughMAC();
                    }
                });
        builder.show();
    }

    public BluetoothSocket getSocket()
    {
        return this.conn_t.mmSocket;
    }

    private class ConnectThread extends Thread
    {
        public final BluetoothSocket mmSocket;
        private final BluetoothDevice mmDevice;

        public ConnectThread(BluetoothDevice device)
        {
            // Create a temp socket because mmSocket is final
            BluetoothSocket temp = null;
            this.mmDevice = device;

            // Get a BluetoothSocket to connect with the given BluetoothDevice
            try {
                // UUID is specific to the ELM327
                temp = this.mmDevice.createRfcommSocketToServiceRecord(UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"));
            }
            catch (IOException e) {
                conn_status = false;
                Log.d("UUID_ERROR", "Error from UUID creating Bluetooth connecting Socket");
            }
            this.mmSocket = temp;
        }

        public void run() {
            // Cancel discovery because it will slow down the connection
            mBlAdapter.cancelDiscovery();

            try {
                // Connect the device through the socket. This will block
                // until it succeeds or throws an exception
                mmSocket.connect();
                conn_status = true;
            } catch (IOException connectException) {
                conn_status = false;
                Log.d("IO_ERROR", "Error from IO creating Bluetooth connecting Socket " + connectException.toString());
                try {
                    mmSocket.close();
                } catch (IOException closeException) { }
                return;
            }
        }

        public void cancel() {
            try {
                conn_status = false;
                mmSocket.close();
            } catch (IOException e) { }
        }
    }
}

package org.ennen.enomoto;

import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.DialogInterface;
import android.content.Intent;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Set;

/**
 * Created by asmateus on 15/10/16.
 */

public class BluetoothConnector
{
    private static final int REQUEST_ENABLE_BT = 1;
    private ArrayList<String> paired_adapter_list = new ArrayList<>();
    private MainActivity master;

    public BluetoothConnector(MainActivity master)
    {
        this.master = master;
        BluetoothAdapter mBlAdapter = BluetoothAdapter.getDefaultAdapter();
        if (mBlAdapter == null) {
            Toast toast = Toast.makeText(master.getApplicationContext(), "Bluetooth not Supported", Toast.LENGTH_LONG);
            toast.show();
        }
        else {
            if (!mBlAdapter.isEnabled()) {
                Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                master.startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
            }
            else
                searchPairedDevices(mBlAdapter);
        }
    }

    private void searchPairedDevices(BluetoothAdapter mBlAdapter)
    {
        Set<BluetoothDevice> pairedDevices = mBlAdapter.getBondedDevices();
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
                    // the user clicked on colors[which]
                }
        });
        builder.show();
    }
}

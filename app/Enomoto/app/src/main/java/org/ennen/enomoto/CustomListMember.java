package org.ennen.enomoto;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.content.Context;
import android.util.Log;
import android.view.ContextMenu;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ListAdapter;
import android.widget.TextView;

import java.util.ArrayList;

/**
 * Created by asmateus on 14/10/16.
 */

public class CustomListMember extends BaseAdapter implements ListAdapter {
    private ArrayList<String> list = new ArrayList<>();
    private Context context;

    public CustomListMember(ArrayList<String> list, Context context) {
        this.list = list;
        this.context = context;

        // Hide delete button on start
    }

    public void addItem(String task)
    {
        this.list.add(task);
    }

    @Override
    public int getCount() {
        return list.size();
    }

    @Override
    public Object getItem(int pos) {
        return list.get(pos);
    }

    @Override
    public long getItemId(int pos) {
        return 0;
        //return list.get(pos).getId();
        //just return 0 if your list items do not have an Id variable.
    }

    @Override
    public View getView(final int position, View convertView, ViewGroup parent) {
        View view = convertView;
        if (view == null) {
            LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
            view = inflater.inflate(R.layout.list_item, null);
        }

        //Handle TextView and display string from your list
        TextView listItemText = (TextView)view.findViewById(R.id.list_item_string);
        listItemText.setText(list.get(position));

        //Handle buttons and add onClickListeners
        ImageButton deleteBtn = (ImageButton)view.findViewById(R.id.delete_btn);

        deleteBtn.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                //do something
                list.remove(position); //or some other task
                notifyDataSetChanged();
            }
        });

        view.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                toogleButton(v);
            }
        });

        return view;
    }

    public void toogleButton(View v) {
        ImageButton btn = (ImageButton)v.findViewById(R.id.delete_btn);
        if(btn.getVisibility() == View.GONE) {
            btn.setClickable(true);
            btn.setVisibility(View.VISIBLE);
        }
        else {
            btn.setClickable(false);
            btn.setVisibility(View.GONE);
        }
    }
}

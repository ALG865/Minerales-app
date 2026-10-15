package es.csic.mineralesestrategicos;

import android.webkit.WebSettings;
import android.webkit.WebView;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    private void ajustarWebView() {
        if (getBridge() == null) return;
        WebView w = getBridge().getWebView();
        if (w == null) return;
        WebSettings s = w.getSettings();
        // Que el tamaño de letra del sistema no agrande la web: la app usa siempre su propio tamaño.
        s.setTextZoom(100);
        // Zoom con dos dedos, sin los botones +/- en pantalla.
        s.setUseWideViewPort(true);
        s.setSupportZoom(true);
        s.setBuiltInZoomControls(true);
        s.setDisplayZoomControls(false);
    }

    @Override
    public void onStart() { super.onStart(); ajustarWebView(); }

    @Override
    public void onResume() { super.onResume(); ajustarWebView(); }
}

#include "flutter_window.h"
#include <optional>
#include <mutex>
#include <dwmapi.h>
#include <flutter/method_channel.h>
#include <flutter/standard_method_codec.h>
#include "flutter/generated_plugin_registrant.h"
#include "utils.h"

#ifndef DWMWA_USE_IMMERSIVE_DARK_MODE
#define DWMWA_USE_IMMERSIVE_DARK_MODE 20
#endif

constexpr const wchar_t kGetPreferredBrightnessRegKey[] =
  L"Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize";
constexpr const wchar_t kGetPreferredBrightnessRegValue[] = L"AppsUseLightTheme";

FlutterWindow::FlutterWindow(const flutter::DartProject& project)
    : project_(project) {}

FlutterWindow::~FlutterWindow() {}

bool FlutterWindow::OnCreate() {
    if (!Win32Window::OnCreate()) {
        return false;
    }

    RECT frame = GetClientArea();
    flutter_controller_ = std::make_unique<flutter::FlutterViewController>(
        frame.right - frame.left, frame.bottom - frame.top, project_);
    if (!flutter_controller_->engine() || !flutter_controller_->view()) {
        return false;
    }
    RegisterPlugins(flutter_controller_->engine());
    SetChildContent(flutter_controller_->view()->GetNativeWindow());

    static std::mutex visible_mutex;
    static bool visible = false;

    flutter_controller_->engine()->SetNextFrameCallback([&]() {
        std::scoped_lock lock(visible_mutex);
        this->Show();
        visible = true;
    });

    flutter::MethodChannel<> channel(
        flutter_controller_->engine()->messenger(), "tests.flutter.dev/windows_startup_test",
        &flutter::StandardMethodCodec::GetInstance());

    channel.SetMethodCallHandler(
    [&](const flutter::MethodCall<>& call,
       std::unique_ptr<flutter::MethodResult<>> result) {
       std::string method = call.method_name();

      if (method == "isWindowVisible") {
        std::scoped_lock lock(visible_mutex);
        result->Success(visible);
      } else if (method == "isAppDarkModeEnabled") {
        BOOL enabled;
        HRESULT hr = DwmGetWindowAttribute(GetHandle(),
                                           DWMWA_USE_IMMERSIVE_DARK_MODE,
                                           &enabled, sizeof(enabled));
        if (SUCCEEDED(hr)) {
          result->Success((bool)enabled);
        } else if (hr == E_INVALIDARG) {
          result->Success(false);
        } else {
          result->Error("error", "Received result handle " + hr);
        }
      } else if (method == "isSystemDarkModeEnabled") {
        DWORD data;
        DWORD data_size = sizeof(data);
        LONG status = RegGetValue(HKEY_CURRENT_USER,
                                  kGetPreferredBrightnessRegKey,
                                  kGetPreferredBrightnessRegValue,
                                  RRF_RT_REG_DWORD, nullptr, &data, &data_size);

        if (status == ERROR_SUCCESS) {
          result->Success(data == 0);
        } else if (status == ERROR_FILE_NOT_FOUND) {
          result->Success(false);
        } else {
          result->Error("error", "Received status " + status);
        }
      } else if (method == "convertString") {
        const flutter::EncodableValue* argument = call.arguments();
        const std::vector<int32_t> code_points = std::get<std::vector<int32_t>>(*argument);
        std::vector<wchar_t> wide_str;
        for (int32_t code_point : code_points) {
          wide_str.push_back((wchar_t)(code_point));
        }
        wide_str.push_back((wchar_t)0);
        const std::string string = Utf8FromUtf16(wide_str.data());
        result->Success(string);
      } else {
        result->NotImplemented();
      }
    });

    return true;
}

void FlutterWindow::OnDestroy() {
    if (flutter_controller_) {
        flutter_controller_ = nullptr;
    }

    Win32Window::OnDestroy();
}

LRESULT
FlutterWindow::MessageHandler(HWND hwnd, UINT const message,
                              WPARAM const wparam,
                              LPARAM const lparam) noexcept {
    if (flutter_controller_) {
        std::optional<LRESULT> result =
            flutter_controller_->HandleTopLevelWindowProc(hwnd, message, wparam,
                                                          lparam);
        if (result) {
            return *result;
        }
    }

    switch (message) {
        case WM_FONTCHANGE:
            flutter_controller_->engine()->ReloadSystemFonts();
            break;
    }

    return Win32Window::MessageHandler(hwnd, message, wparam, lparam);
}

import { create } from "zustand";
import { mountStoreDevtool } from "simple-zustand-devtools";

const useAuthStore = create((set, get) => ({
  allUserData: null,
  loading: false,
  isLoggedIn: false,
  user: null,

  setUser: (user) =>
    set({
      allUserData: user,
      isLoggedIn: user !== null,
      user: user
        ? {
            user_id: user.user_id,
            username: user.username,
          }
        : null,
    }),
  setLoading: (loading) => set({ loading }),
}));

// For development only
if (process.env.NODE_ENV === 'development') {
    mountStoreDevtool("Store", useAuthStore);
  }

export { useAuthStore };
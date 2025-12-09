<script lang="ts">
	import * as Tooltip from "$lib/components/ui/tooltip/index.js";
	import { cn, type WithElementRef } from "$lib/utils.js";
	import { onMount } from "svelte";
	import type { HTMLAttributes } from "svelte/elements";
	import {
	  SIDEBAR_COOKIE_MAX_AGE,
	  SIDEBAR_COOKIE_NAME,
	  SIDEBAR_WIDTH,
	  SIDEBAR_WIDTH_ICON,
	  SIDEBAR_WIDTH_STORAGE_KEY,
	} from "./constants.js";
	import { setSidebar } from "./context.svelte.js";

	let {
		ref = $bindable(null),
		open = $bindable(true),
		onOpenChange = () => {},
		class: className,
		style,
		children,
		...restProps
	}: WithElementRef<HTMLAttributes<HTMLDivElement>> & {
		open?: boolean;
		onOpenChange?: (open: boolean) => void;
	} = $props();

	// Initialize width from localStorage or use default
	let width = $state(SIDEBAR_WIDTH);
	
	onMount(() => {
		if (typeof window !== "undefined") {
			const storedWidth = localStorage.getItem(SIDEBAR_WIDTH_STORAGE_KEY);
			if (storedWidth) {
				width = storedWidth;
			}
		}
	});

	const sidebar = setSidebar({
		open: () => open,
		setOpen: (value: boolean) => {
			open = value;
			onOpenChange(value);

			// This sets the cookie to keep the sidebar state.
			document.cookie = `${SIDEBAR_COOKIE_NAME}=${open}; path=/; max-age=${SIDEBAR_COOKIE_MAX_AGE}`;
		},
		width: () => width,
		setWidth: (value: string) => {
			width = value;
			if (typeof window !== "undefined") {
				localStorage.setItem(SIDEBAR_WIDTH_STORAGE_KEY, value);
			}
		},
	});
</script>

<svelte:window onkeydown={sidebar.handleShortcutKeydown} />

<Tooltip.Provider delayDuration={0}>
	<div
		data-slot="sidebar-wrapper"
		style="--sidebar-width: {width}; --sidebar-width-icon: {SIDEBAR_WIDTH_ICON}; {style}"
		class={cn(
			"group/sidebar-wrapper has-data-[variant=inset]:bg-sidebar flex min-h-svh w-full",
			className
		)}
		bind:this={ref}
		{...restProps}
	>
		{@render children?.()}
	</div>
</Tooltip.Provider>

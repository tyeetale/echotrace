<script lang="ts" module>
  // This is sample data.
  const data = {
    tree: [
      ["convo 1", ["convo 1.1", "convo 1.1.1", "convo 1.1.2"], "convo 1.2"],
      ["convo 2", ["convo 2.1", "convo 2.1.1", "convo 2.1.2"], "convo 2.2"],
      // show super nesting here
      [
        "convo 3",
        [
          "convo 3.1",
          "convo 3.1.1",
          [
            "convo 3.1.1.1",
            "convo 3.1.1.2",
            [
              "convo 3.1.1.1.1",
              "convo 3.1.1.1.2",
              ["convo 3.1.1.1.1.1", "convo 3.1.1.1.1.2", "convo 3.1.1.1.1.3"],
            ],
          ],
        ],
      ],
      "convo 4",
    ],
    timeline: [
      {
        file: "message 1 found here",
        id: "0ac573b",
      },
      {
        file: "message 2 found here",
        id: "23a5b23",
      },
      {
        file: "message 3 found here",
        id: "9876543",
      },
    ],
  };
</script>

<script lang="ts">
  import { Button } from "$lib/components/ui/button/index.js";
  import * as Collapsible from "$lib/components/ui/collapsible/index.js";
  import * as Sidebar from "$lib/components/ui/sidebar/index.js";
  import { cn } from "$lib/utils.js";
  import ChevronDownIcon from "@lucide/svelte/icons/chevron-down";
  import ChevronRightIcon from "@lucide/svelte/icons/chevron-right";
  import MessageCirclePlusIcon from "@lucide/svelte/icons/message-circle-plus";
  import type { ComponentProps } from "svelte";

  let {
    ref = $bindable(null),
    ...restProps
  }: ComponentProps<typeof Sidebar.Root> = $props();
</script>

<Sidebar.Root bind:ref {...restProps}>
  <Sidebar.Header>
    <!-- // add logo flex and a button for creating a new chat -->
    <!-- ensure that the header matches the same height as the content header in the main page -->
    <div class="flex items-center justify-between p-2 h-11.75">
      <!-- // the logo will be a square svg icon -->
      <img src="/logo.svg" alt="EchoTrace" class="h-6 w-6" />

      <!-- // change to button with a lucide write edit icon -->
      <Button variant="outline" size="icon">
        <MessageCirclePlusIcon className="h-4 w-4" />
      </Button>
    </div>
  </Sidebar.Header>
  <Sidebar.Content>
    <Sidebar.Separator />
    <Collapsible.Root open class="group/collapsible">
      <Sidebar.Group>
        <Sidebar.GroupLabel>
          <Collapsible.Trigger class="flex items-center justify-between w-full">
            <span class="truncate min-w-0 pr-2">Chats</span>
            <ChevronDownIcon
              class="ms-auto transition-transform group-data-[state=open]/collapsible:rotate-180 shrink-0 h-4 w-4 text-muted-foreground"
            />
          </Collapsible.Trigger>
        </Sidebar.GroupLabel>
        <Collapsible.Content>
          <Sidebar.GroupContent>
            <Sidebar.Menu>
              {#each data.tree as item, index (index)}
                {@render Tree({ item })}
              {/each}
            </Sidebar.Menu>
          </Sidebar.GroupContent></Collapsible.Content
        >
      </Sidebar.Group></Collapsible.Root
    >

    <Sidebar.Separator />
    <Collapsible.Root open class="group/collapsible">
      <Sidebar.Group>
        <Sidebar.GroupLabel>
          <Collapsible.Trigger class="flex items-center justify-between w-full">
            <span class="truncate min-w-0 pr-2">Timeline</span>
            <ChevronDownIcon
              class="ms-auto transition-transform group-data-[state=open]/collapsible:rotate-180 shrink-0 h-4 w-4 text-muted-foreground"
            />
          </Collapsible.Trigger>
        </Sidebar.GroupLabel>
        <!-- <Sidebar.GroupLabel>Timeline</Sidebar.GroupLabel> -->
        <Collapsible.Content>
          <Sidebar.GroupContent>
            <Sidebar.Menu>
              {#each data.timeline as item, index (index)}
                <Sidebar.MenuItem>
                  <Sidebar.MenuButton class="pr-16">
                    <span class="truncate min-w-0">{item.file}</span>
                  </Sidebar.MenuButton>
                  <Sidebar.MenuBadge class="text-xs text-neutral-400/50"
                    >{item.id}</Sidebar.MenuBadge
                  >
                </Sidebar.MenuItem>
              {/each}
            </Sidebar.Menu>
          </Sidebar.GroupContent></Collapsible.Content
        >
      </Sidebar.Group></Collapsible.Root
    >
  </Sidebar.Content>
  <Sidebar.Rail />
</Sidebar.Root>

<!-- eslint-disable-next-line @typescript-eslint/no-explicit-any -->
{#snippet Tree({ item }: { item: string | any[] })}
  {@const [name, ...items] = Array.isArray(item) ? item : [item]}
  {#if !items.length}
    <Sidebar.MenuButton
      isActive={name === "button.svelte"}
      class="data-[active=true]:bg-transparent min-w-0"
    >
      <span class="truncate min-w-0">{name}</span>
    </Sidebar.MenuButton>
  {:else}
    <Sidebar.MenuItem>
      <Collapsible.Root
        class="group/collapsible [&[data-state=open]>button>svg:last-child]:rotate-90"
        open={name === "lib" || name === "components"}
      >
        <Collapsible.Trigger>
          {#snippet child({ props })}
            {@const existingClass =
              "class" in props ? String(props.class) : undefined}
            {@const buttonClass = cn("min-w-0", existingClass)}
            <Sidebar.MenuButton {...props} class={buttonClass}>
              <span class="truncate min-w-0">{name}</span>
              <ChevronRightIcon className="transition-transform shrink-0" />
            </Sidebar.MenuButton>
          {/snippet}
        </Collapsible.Trigger>
        <Collapsible.Content>
          <Sidebar.MenuSub>
            {#each items as subItem, index (index)}
              {@render Tree({ item: subItem })}
            {/each}
          </Sidebar.MenuSub>
        </Collapsible.Content>
      </Collapsible.Root>
    </Sidebar.MenuItem>
  {/if}
{/snippet}
